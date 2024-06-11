from typing import List, Type, Optional, Any, TypeVar

from psycopg2 import extensions

T = TypeVar('T')


class QueryResult:

    def __init__(self, rows_affected: int) -> None:
        self._rows_affected = rows_affected
        self._columns = []
        self._rows = []
        self._records = []

    @property
    def records(self) -> List[dict]:
        return self._records

    def first(self) -> dict:
        if not self._records:
            return {}
        return self._records[0]

    def map_first_to_model(self, model: Type[T]) -> Optional[T]:
        if not self._records:
            return None
        return model(**self._records[0])

    def map_all_to_model(self, model: Type[T]) -> List[T]:
        return [model(**record) for record in self._records]

    def values_at_column(self, column_name: str) -> List[Any]:
        values = []
        for record in self._records:
            values.append(record[column_name])
        return values

    def is_empty(self) -> bool:
        return len(self._records) == 0

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} [{len(self._records)} records]>'

    @classmethod
    def from_cursor(cls, cursor: extensions.cursor) -> 'QueryResult':
        query_result = QueryResult(cursor.rowcount)
        # If it has no columns, it means the query returned no results
        if not cursor.description:
            return query_result
        query_result._columns = [x.name for x in cursor.description]
        query_result._rows = cursor.fetchall()
        query_result._records = []
        for row in query_result._rows:
            record = {}
            for i, col in enumerate(query_result._columns):
                record[col] = row[i]
            query_result._records.append(record)
        return query_result
