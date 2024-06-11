from _decimal import Decimal
from datetime import datetime
from enum import Enum
from typing import Optional, Union

from src.infrastructure.utils.db.pg_function import PGFunction

PostgresValue = Optional[Union[datetime, dict, bool, int, float, Decimal, list, tuple, str, Enum, PGFunction]]
