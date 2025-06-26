import logging
from typing import List

from core.entities.video import Video
from core.interfaces.data_loader import DataLoader
from core.interfaces.dislike_api import DislikeApi
from core.interfaces.youtube_api import YouTubeApi

logger = logging.getLogger(__name__)


class FetchAndLoadTrends:
    def __init__(
        self,
        youtube_api: YouTubeApi,
        dislike_api: DislikeApi,
        data_loader: DataLoader,
    ):
        self._youtube_api = youtube_api
        self._dislike_api = dislike_api
        self._data_loader = data_loader

    def execute(self, region_code: str):
        logger.info(f"Fetching trending videos for region: {region_code}")
        videos = self._youtube_api.get_popular_videos(region_code)
        if not videos:
            logger.warning("No videos found. Aborting.")
            return

        categories = self._youtube_api.get_categories(region_code)
        category_map = {cat.id: cat.title for cat in categories}

        enriched_videos: List[Video] = []
        for video in videos:
            video.category_name = category_map.get(video.category_id)

            dislikes_data = self._dislike_api.get_dislikes(video.id)
            if dislikes_data:
                video.dislike_count, video.rating = dislikes_data
            
            enriched_videos.append(video)

        logger.info(f"Enriched {len(enriched_videos)} videos.")
        self._data_loader.load(enriched_videos)
        logger.info("ETL process finished.") 