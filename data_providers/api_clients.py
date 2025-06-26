import logging
from typing import List, Optional, Tuple

import requests
from requests import Session

from core.entities.category import Category
from core.entities.video import Video
from core.interfaces.dislike_api import DislikeApi
from core.interfaces.youtube_api import YouTubeApi

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YouTubeApiProvider(YouTubeApi):
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._session: Session = requests.Session()
        self._session.params = {"key": self._api_key}

    def get_popular_videos(
        self, region_code: str, max_results: int = 50
    ) -> List[Video]:
        """Fetches most popular videos from YouTube API."""
        endpoint = f"{self.BASE_URL}/videos"
        params = {
            "part": "id,statistics,snippet",
            "chart": "mostPopular",
            "regionCode": region_code,
            "maxResults": max_results,
        }
        try:
            response = self._session.get(endpoint, params=params)
            response.raise_for_status()
            raw_data = response.json()
            return self._parse_videos(raw_data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching popular videos: {e}")
            return []

    def get_categories(self, region_code: str) -> List[Category]:
        """Fetches video categories from YouTube API."""
        endpoint = f"{self.BASE_URL}/videoCategories"
        params = {"part": "snippet", "regionCode": region_code}
        try:
            response = self._session.get(endpoint, params=params)
            response.raise_for_status()
            raw_data = response.json()
            return self._parse_categories(raw_data)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching categories: {e}")
            return []

    def _parse_videos(self, raw_data: dict) -> List[Video]:
        videos = []
        for item in raw_data.get("items", []):
            try:
                video = Video(
                    id=item["id"],
                    title=item["snippet"]["title"],
                    upload_date=item["snippet"]["publishedAt"].split("T")[0],
                    view_count=int(item["statistics"].get("viewCount", 0)),
                    like_count=int(item["statistics"].get("likeCount", 0)),
                    comment_count=int(item["statistics"].get("commentCount", 0)),
                    category_id=item["snippet"]["categoryId"],
                )
                videos.append(video)
            except (KeyError, TypeError) as e:
                logger.warning(f"Skipping video due to parsing error: {e}")
        return videos

    def _parse_categories(self, raw_data: dict) -> List[Category]:
        categories = []
        for item in raw_data.get("items", []):
            try:
                category = Category(
                    id=item["id"], title=item["snippet"]["title"]
                )
                categories.append(category)
            except (KeyError, TypeError) as e:
                logger.warning(f"Skipping category due to parsing error: {e}")
        return categories


class DislikeApiProvider(DislikeApi):
    BASE_URL = "https://returnyoutubedislikeapi.com/votes"

    def __init__(self):
        self._session: Session = requests.Session()

    def get_dislikes(self, video_id: str) -> Optional[Tuple[int, float]]:
        """Fetches dislike count for a video."""
        params = {"videoId": video_id}
        try:
            response = self._session.get(self.BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("dislikes"), data.get("rating")
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching dislikes for video {video_id}: {e}")
        except (KeyError, TypeError) as e:
            logger.error(f"Error parsing dislike data for video {video_id}: {e}")
        return None 