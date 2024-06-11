from typing import List

from src.domain.models.measure import Measure
from src.domain.repositories.measure_repository import MeasureRepository


class MeasureRetriever:
    _MAX_MEASURES = 200

    def __init__(self, measure_repository: MeasureRepository) -> None:
        self._measure_repository = measure_repository

    def get_recent_measures(self) -> List[Measure]:
        measures = self._measure_repository.get_latest(self._MAX_MEASURES)
        return sorted(measures, key=lambda x: x.timestamp)
