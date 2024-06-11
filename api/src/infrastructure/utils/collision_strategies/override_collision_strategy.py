from typing import Union, Dict

from src.infrastructure.utils.collision_strategies.base_collision_strategy import BaseCollisionStrategy
from src.infrastructure.utils.key import Key
from src.infrastructure.utils.postgres_value import PostgresValue
from src.infrastructure.utils.query_utils import generate_update_clauses


class OverrideCollisionStrategy(BaseCollisionStrategy):

    @classmethod
    def _collision_resolution_query(cls, column_mappings: Dict[Union[Key, str], PostgresValue]) -> str:
        update_clauses = generate_update_clauses(column_mappings)
        return f"""UPDATE SET {', '.join(update_clauses)}"""
