import psycopg2
from psycopg2.extensions import connection
from contextlib import contextmanager

from src.config.config_provider import ConfigProvider


def get_psycopg2_connection(specify_database: bool = True) -> connection:
    kwargs = {
        'host': ConfigProvider.DB_HOST,
        'user': ConfigProvider.DB_USER,
        'password': ConfigProvider.DB_PASSWORD,
        'port': ConfigProvider.DB_PORT,
    }
    if specify_database:
        kwargs['database'] = ConfigProvider.DB_NAME
    return psycopg2.connect(**kwargs)


@contextmanager
def psycopg2_session_scope():
    conn = psycopg2.connect(
        host=ConfigProvider.DB_HOST,
        database=ConfigProvider.DB_NAME,
        user=ConfigProvider.DB_USER,
        password=ConfigProvider.DB_PASSWORD,
        port=ConfigProvider.DB_PORT,
        # Adding these because the server keeps terminating prematurely on long-running queries
        keepalives=1,
        keepalives_idle=30,
        keepalives_interval=10,
        keepalives_count=5
    )
    try:
        yield conn
        conn.commit()
    except Exception as err:
        conn.rollback()
        conn.close()
        raise err
    finally:
        conn.close()
