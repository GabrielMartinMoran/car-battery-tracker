from enum import Enum

from src.infrastructure.utils.collision_strategies.fail_collision_strategy import FailCollisionStrategy
from src.infrastructure.utils.collision_strategies.ignore_collision_strategy import IgnoreCollisionStrategy
from src.infrastructure.utils.collision_strategies.override_collision_strategy import OverrideCollisionStrategy


class CollisionStrategy(Enum):
    FAIL = FailCollisionStrategy()
    IGNORE = IgnoreCollisionStrategy()
    OVERRIDE = OverrideCollisionStrategy()
