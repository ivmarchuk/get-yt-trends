from abc import ABC, abstractmethod
from typing import List

from core.entities.category import Category
from core.entities.video import Video


class YouTubeApi(ABC):
    @abstractmethod
    def get_popular_videos(
        self, region_code: str, max_results: int = 50
    ) -> List[Video]:
        pass

    @abstractmethod
    def get_categories(self, region_code: str) -> List[Category]:
        pass 