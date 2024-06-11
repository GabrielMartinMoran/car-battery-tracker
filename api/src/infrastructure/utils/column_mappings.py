from typing import List, Dict, Union, Optional

from pydantic import BaseModel

from src.infrastructure.utils.key import Key
from src.infrastructure.utils.postgres_value import PostgresValue

ColumnMappings = Dict[Union[Key, str], PostgresValue]


def build_column_mapping_from_model(model: BaseModel, keys: List[str] = None,
                                    extra: Optional[ColumnMappings] = None) -> ColumnMappings:
    _keys = keys if keys is not None else []
    _extra = extra if extra is not None else {}
    dumped = model.model_dump()
    column_mapping = {}
    for k, v in (list(dumped.items()) + list(_extra.items())):
        if k in _keys:
            column_mapping[Key(k)] = v
        else:
            column_mapping[k] = v
    return column_mapping
