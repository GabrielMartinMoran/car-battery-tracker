import json
from _decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Iterable, Dict, Union, List

from src.infrastructure.utils.db.pg_function import PGFunction
from src.utils import dates
from src.infrastructure.utils.key import Key
from src.infrastructure.utils.postgres_value import PostgresValue


def str_tuple(items: Iterable[str]) -> str:
    return f"({', '.join(items)})"


def escape(value: str) -> str:
    return value.replace("'", "''")


def stringify(value: PostgresValue) -> str:
    if value is None:
        return 'null'
    if isinstance(value, datetime):
        return f"'{dates.to_utc_isostring(value)}'::TIMESTAMP"
    if isinstance(value, dict):
        return f"'{escape(json.dumps(value))}'"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, (int, float, Decimal)):
        return str(value)
    if isinstance(value, (list, tuple)):
        if len(value) > 0:
            return f"""ARRAY {f"[{', '.join([stringify(x) for x in value])}]"}"""
        return "'{}'"
    if isinstance(value, Enum):
        return f"'{escape(value.value)}'"
    if isinstance(value, PGFunction):
        return f'{value.function}'
    return f"'{escape(value)}'"


def generate_update_clauses(column_mappings: Dict[Union[Key, str], PostgresValue], map_keys: bool = False) -> List[str]:
    update_clauses = []
    for column, value in column_mappings.items():
        if not isinstance(column, Key) or (isinstance(column, Key) and map_keys):
            update_clauses.append(f'{column} = {stringify(value)}')
    return update_clauses
