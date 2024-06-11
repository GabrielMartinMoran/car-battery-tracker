from typing import Optional, Dict, Union, List, TypeVar

import psycopg2
from psycopg2.extensions import connection
from pypika import Query
from pypika.queries import QueryBuilder

from src.infrastructure.exceptions.already_exists_exception import AlreadyExistsException
from src.infrastructure.utils.collision_strategies.collision_strategy import CollisionStrategy
from src.infrastructure.utils.column_mappings import ColumnMappings
from src.infrastructure.utils.db.pg_connection import get_psycopg2_connection, psycopg2_session_scope
from src.infrastructure.utils.postgres_value import PostgresValue
from src.infrastructure.utils.query_builder import build_insert_query, build_delete_query, build_select_query, \
    build_update_query
from src.infrastructure.utils.query_result import QueryResult

T = TypeVar('T')


class PGTransaction(connection):
    pass


class PostgresRepository:

    @classmethod
    def _execute_query(cls, query: Union[QueryBuilder, str],
                       transaction: Optional[PGTransaction] = None) -> QueryResult:
        conn = transaction
        if conn is None:
            conn = get_psycopg2_connection()
        try:
            cursor = conn.cursor()
            _query = str(query) if isinstance(query, QueryBuilder) else query
            cursor.execute(_query)
            query_result = QueryResult.from_cursor(cursor)
            if transaction is None:
                conn.commit()
        except Exception as e:
            if transaction is None:
                conn.rollback()
            raise Exception(e)
        finally:
            if transaction is None:
                conn.close()
        return query_result

    def _insert(self, table_name: str, column_mappings: ColumnMappings, returning: List[str] = None,
                collision_strategy: CollisionStrategy = CollisionStrategy.FAIL,
                transaction: Optional[PGTransaction] = None) -> Optional[QueryResult]:
        query = build_insert_query(table_name, column_mappings, collision_strategy)
        if returning is not None:
            query += f''' RETURNING {", ".join(returning)}'''
        try:
            query_result = self._execute_query(query, transaction)
        except Exception as e:
            if isinstance(e.args[0], psycopg2.errors.UniqueViolation):
                raise AlreadyExistsException()
            raise
        if returning is not None:
            return query_result

    def _delete(self, table_name: str, filters: Dict[str, PostgresValue],
                transaction: Optional[PGTransaction] = None) -> None:
        query = build_delete_query(table_name, filters)
        self._execute_query(query, transaction)

    def _select(self, table_name: str, filters: Dict[str, PostgresValue] = None, columns: List[str] = None,
                transaction: Optional[PGTransaction] = None) -> QueryResult:
        query = build_select_query(table_name, filters, columns)
        return self._execute_query(query, transaction)

    def _bulk_insert(self, table_name: str, records_column_mappings: List[ColumnMappings],
                     collision_strategy: CollisionStrategy = CollisionStrategy.IGNORE,
                     transaction: Optional[PGTransaction] = None) -> None:
        queries = [
            build_insert_query(table_name, column_mappings, collision_strategy) for column_mappings in
            records_column_mappings
        ]
        self._bulk_execute(queries, transaction)

    def _update(self, table_name: str, column_mappings: ColumnMappings,
                transaction: Optional[PGTransaction] = None) -> None:
        query = build_update_query(table_name, column_mappings)
        self._execute_query(query, transaction)

    def _bulk_execute(self, queries: List[str], transaction: Optional[PGTransaction] = None) -> None:
        query = '; '.join(queries)
        self._execute_query(query, transaction)

    @classmethod
    def create_transaction(cls) -> PGTransaction:
        return psycopg2_session_scope()
