from dataclasses import dataclass
from typing import Dict, Union, List, Any

from src.infrastructure.utils.collision_strategies.collision_strategy import CollisionStrategy
from src.infrastructure.utils.column_mappings import ColumnMappings
from src.infrastructure.utils.db.pg_function import PGFunction
from src.infrastructure.utils.key import Key
from src.infrastructure.utils.postgres_value import PostgresValue
from src.infrastructure.utils.query_utils import stringify, str_tuple


@dataclass
class ColumnsMapping:
    columns: List[str]
    values: List[Any]
    keys_count: int

    @classmethod
    def from_dict(cls, column_mappings: Dict[Union[Key, str], PostgresValue]) -> 'ColumnsMapping':
        assert len(column_mappings) > 0, 'At least one column must be provided'
        keys_count = 0
        columns = []
        values = []
        for column, value in column_mappings.items():
            if isinstance(column, Key):
                keys_count += 1
                columns.append(column.name)
            else:
                columns.append(column)
            if isinstance(value, PGFunction):
                values.append(value.function)
            else:
                values.append(stringify(value))

        return ColumnsMapping(
            columns=columns,
            values=values,
            keys_count=keys_count
        )


def build_insert_query(table_name: str, column_mappings: ColumnMappings,
                       collision_strategy: CollisionStrategy) -> str:
    mapping = ColumnsMapping.from_dict(column_mappings)

    query = f"INSERT INTO {table_name} {str_tuple(mapping.columns)} VALUES {str_tuple(mapping.values)}"

    if mapping.keys_count > 0:
        query += f' {collision_strategy.value.generate_query(column_mappings)}'

    return query


def build_delete_query(table_name: str, filters: Dict[str, PostgresValue]) -> str:
    mapping = ColumnsMapping.from_dict(filters)

    return (f"DELETE FROM {table_name} WHERE "
            f"{' AND '.join([f'{mapping.columns[i]}={mapping.values[i]}' for i in range(len(mapping.columns))])}")


def build_select_query(table_name: str, filters: Dict[str, PostgresValue] = None, columns: List[str] = None) -> str:
    if filters is not None:
        mapping = ColumnsMapping.from_dict(filters)
        mapping_str = ' AND '.join([f'{mapping.columns[i]}={mapping.values[i]}' for i in range(len(mapping.columns))])
        filters_str = f"WHERE {mapping_str}"
    else:
        filters_str = ''

    if columns is None:
        included_columns = '*'
    else:
        included_columns = ', '.join(columns)

    return f"SELECT {included_columns} FROM {table_name} {filters_str}"


def build_update_query(table_name: str, column_mappings: ColumnMappings) -> str:
    keys = {}
    other_columns = {}
    for k, v in column_mappings.items():
        if isinstance(k, Key):
            keys[k] = v
        else:
            other_columns[k] = v

    keys_mapping = ColumnsMapping.from_dict(keys)
    other_columns_mapping = ColumnsMapping.from_dict(other_columns)

    keys_filter_str = ' AND '.join(
        [f'{keys_mapping.columns[i]}={keys_mapping.values[i]}' for i in range(len(keys_mapping.columns))]
    )
    columns_set_str = ', '.join([f'{other_columns_mapping.columns[i]}={other_columns_mapping.values[i]}' for i in
                                 range(len(other_columns_mapping.columns))])

    return f"UPDATE {table_name} SET {columns_set_str} WHERE {keys_filter_str}"
