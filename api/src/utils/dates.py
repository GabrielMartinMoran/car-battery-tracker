from datetime import datetime, timezone
from dateutil import parser


def now() -> datetime:
    return datetime.now().astimezone(timezone.utc)


def to_datetime(str_date: str) -> datetime:
    dt = parser.parse(str_date)
    return dt.replace(tzinfo=timezone.utc)


def to_utc_isostring(dt: datetime) -> str:
    """
    Returns data as string with format like: 2021-07-26T16:05:09.923716+00:00
    """
    return dt.replace(tzinfo=timezone.utc).isoformat()
