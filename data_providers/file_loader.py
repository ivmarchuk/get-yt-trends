import logging
import pandas as pd
from typing import List
from dataclasses import asdict

from core.entities.video import Video
from core.interfaces.data_loader import DataLoader

logger = logging.getLogger(__name__)


class CsvDataLoader(DataLoader):
    def __init__(self, output_path: str):
        self.output_path = output_path

    def load(self, videos: List[Video]):
        if not videos:
            logger.warning("No videos to load.")
            return

        try:
            df = pd.DataFrame([asdict(video) for video in videos])
            df.to_csv(self.output_path, index=False, sep=";", encoding="utf-8")
            logger.info(f"Successfully saved {len(videos)} videos to {self.output_path}")
        except Exception as e:
            logger.error(f"Error saving data to CSV: {e}") 