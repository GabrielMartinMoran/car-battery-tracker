import json
import os
from typing import List

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pypika import Query, Table

from src.config.config_provider import ConfigProvider
from src.infrastructure.db.db_migration import DBMigration
from src.infrastructure.repositories.postgres.postgres_repository import PostgresRepository
from src.infrastructure.utils.collision_strategy import CollisionStrategy
from src.infrastructure.utils.db.pg_connection import get_psycopg2_connection
from src.infrastructure.utils.key import Key


class DBMigrator(PostgresRepository):
    _MIGRATIONS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations')
    _EXTENSION = 'sql'
    _APP_TABLE_NAME = 'app_info'

    def __init__(self) -> None:
        self._create_db_if_not_exists()
        self._migrations = self._get_migrations()
        self._app_table_name_with_schema = f'{ConfigProvider.DB_SCHEMA}.{self._APP_TABLE_NAME}'
        self._app_table = Table(self._APP_TABLE_NAME, schema=ConfigProvider.DB_SCHEMA)
        self._last_migration_number = self._get_last_migration_number()

    @classmethod
    def _create_db_if_not_exists(cls) -> None:
        conn = get_psycopg2_connection(specify_database=False)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"SELECT COUNT(DATNAME) FROM PG_CATALOG.PG_DATABASE WHERE LOWER(DATNAME) = "
                f"LOWER('{ConfigProvider.DB_NAME}')"
            )
            db_exists = cursor.fetchone()[0] > 0
            if not db_exists:
                cursor.execute(f"CREATE DATABASE {ConfigProvider.DB_NAME}")
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {ConfigProvider.DB_SCHEMA}")
        except Exception as e:
            raise Exception(e)
        finally:
            conn.close()

    def apply_pending(self) -> None:
        for migration in self._migrations:
            if migration.number <= self._last_migration_number:
                print(f'> Skipping migration {migration.number}')
            else:
                print(f'> Applying migration {migration.number}')
                self._apply_migration(migration)

    def _get_migrations(self) -> List[DBMigration]:
        return sorted(
            [DBMigration.from_str(x) for x in os.listdir(self._MIGRATIONS_PATH) if x.endswith(f'.{self._EXTENSION}')],
            key=lambda x: x.number
        )

    def _get_last_migration_number(self) -> int:
        try:
            query = Query.from_(self._app_table).select('*').where(self._app_table.key == 'last_migration')
            result = self._execute_query(query)
            return result.first()['value']
        except Exception:
            return 0

    def _apply_migration(self, migration: DBMigration) -> None:
        with open(os.path.join(self._MIGRATIONS_PATH, migration.path), 'r', encoding='utf-8') as f:
            sql = f.read()
        sql = sql.replace('{{schema}}', ConfigProvider.DB_SCHEMA)
        with self.create_transaction() as transaction:
            self._execute_query(sql, transaction)
            self._insert(
                self._app_table_name_with_schema,
                {Key('key'): 'last_migration', 'value': json.dumps(migration.number)},
                collision_strategy=CollisionStrategy.OVERRIDE,
                transaction=transaction
            )
