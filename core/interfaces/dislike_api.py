from abc import ABC, abstractmethod
from typing import Optional, Tuple


class DislikeApi(ABC):
    @abstractmethod
    def get_dislikes(self, video_id: str) -> Optional[Tuple[int, float]]:
        """Returns dislike count and rating."""
        pass 