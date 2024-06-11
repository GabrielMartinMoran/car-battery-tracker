from typing import List

from pypika import Table, Query, Order

from src.config.config_provider import ConfigProvider
from src.domain.models.measure import Measure
from src.domain.repositories.measure_repository import MeasureRepository
from src.infrastructure.repositories.postgres.postgres_repository import PostgresRepository
from src.infrastructure.utils.key import Key


class MeasurePGRepository(MeasureRepository, PostgresRepository):

    def __init__(self) -> None:
        super().__init__()
        self._table_name = 'measure'
        self._table_name_with_schema = f'{ConfigProvider.DB_SCHEMA}.{self._table_name}'
        self._table = Table(self._table_name, schema=ConfigProvider.DB_SCHEMA)

    def put(self, measure: Measure) -> None:
        self._insert(
            self._table_name_with_schema,
            {
                Key('measure_id'): measure.measure_id,
                'timestamp': measure.timestamp,
                'voltage': measure.voltage
            }
        )

    def get_latest(self, size: int) -> List[Measure]:
        query = Query().from_(self._table).select(self._table.star).orderby(self._table.timestamp,
                                                                            order=Order.desc).limit(size)
        result = self._execute_query(query)
        return result.map_all_to_model(Measure)
