from src.domain.models.measure import Measure
from src.domain.repositories.measure_repository import MeasureRepository


class MeasurePersister:

    def __init__(self, measure_repository: MeasureRepository) -> None:
        self._measure_repository = measure_repository

    def track_measure(self, measure: Measure) -> None:
        self._measure_repository.put(measure)
