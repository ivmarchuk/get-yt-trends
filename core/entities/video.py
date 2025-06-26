from dataclasses import dataclass
from typing import Optional


@dataclass
class Video:
    id: str
    title: str
    upload_date: str
    view_count: int
    like_count: int
    comment_count: int
    category_id: str
    category_name: Optional[str] = None
    dislike_count: Optional[int] = None
    rating: Optional[float] = None 