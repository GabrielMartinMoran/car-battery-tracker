from abc import ABC, abstractmethod
from typing import List

from src.domain.models.measure import Measure


class MeasureRepository(ABC):

    @abstractmethod
    def put(self, measure: Measure) -> None: ...

    @abstractmethod
    def get_latest(self, size: int) -> List[Measure]: ...
