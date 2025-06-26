import configparser
import logging
import os
import sys

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.use_cases.fetch_and_load_trends import FetchAndLoadTrends
from data_providers.api_clients import DislikeApiProvider, YouTubeApiProvider
from data_providers.file_loader import CsvDataLoader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    config = configparser.ConfigParser()
    config.read("get-yt-trends/config/pipeline.conf")

    try:
        api_key = config.get("youtube_api", "api_key")
        region_code = config.get("youtube_api", "region_code")
        output_path = config.get("data", "output_path")
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        logging.error(f"Configuration error: {e}")
        return

    # Initialize providers and loader
    youtube_api_provider = YouTubeApiProvider(api_key=api_key)
    dislike_api_provider = DislikeApiProvider()
    csv_loader = CsvDataLoader(output_path=output_path)

    # Initialize and execute the use case
    use_case = FetchAndLoadTrends(
        youtube_api=youtube_api_provider,
        dislike_api=dislike_api_provider,
        data_loader=csv_loader,
    )
    use_case.execute(region_code=region_code)


if __name__ == "__main__":
    main() 