from abc import ABC, abstractmethod
from typing import Dict, Union

from src.infrastructure.utils.key import Key
from src.infrastructure.utils.postgres_value import PostgresValue
from src.infrastructure.utils.query_utils import str_tuple


class BaseCollisionStrategy(ABC):

    def generate_query(self, column_mappings: Dict[Union[Key, str], PostgresValue]) -> str:
        keys = [x.name for x in column_mappings.keys() if isinstance(x, Key)]
        return f"ON CONFLICT {str_tuple(keys)} DO {self._collision_resolution_query(column_mappings)}"

    @abstractmethod
    def _collision_resolution_query(self, column_mappings: Dict[Union[Key, str], PostgresValue]) -> str: pass
