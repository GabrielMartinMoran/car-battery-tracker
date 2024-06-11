from typing import Dict, Union

from src.infrastructure.utils.collision_strategies.base_collision_strategy import BaseCollisionStrategy
from src.infrastructure.utils.key import Key
from src.infrastructure.utils.postgres_value import PostgresValue


class IgnoreCollisionStrategy(BaseCollisionStrategy):

    @classmethod
    def _collision_resolution_query(cls, column_mappings: Dict[Union[Key, str], PostgresValue]) -> str:
        return 'NOTHING'
