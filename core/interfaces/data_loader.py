from abc import ABC, abstractmethod
from typing import List

from core.entities.video import Video


class DataLoader(ABC):
    @abstractmethod
    def load(self, videos: List[Video]):
        pass 