from typing import Dict, Union

from src.infrastructure.utils.collision_strategies.base_collision_strategy import BaseCollisionStrategy
from src.infrastructure.utils.key import Key
from src.infrastructure.utils.postgres_value import PostgresValue


class FailCollisionStrategy(BaseCollisionStrategy):

    def generate_query(self, column_mappings: Dict[Union[Key, str], PostgresValue]) -> str:
        # Do nothing
        return ''

    def _collision_resolution_query(self, column_mappings: Dict[Union[Key, str], PostgresValue]) -> str:
        pass
