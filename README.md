# YouTube Trends ETL

This project is an ETL (Extract, Transform, Load) pipeline that fetches trending YouTube videos, enriches the data with category information and dislike counts, and saves the result to a CSV file.

The project is structured following Clean Architecture principles to ensure separation of concerns, maintainability, and testability.

## Project Structure

-   `core/`: Contains the core business logic of the application.
    -   `entities/`: Defines the core data structures (e.g., `Video`, `Category`).
    -   `interfaces/`: Defines the contracts (abstract base classes) for data providers and loaders.
    -   `usecases/`: Orchestrates the application's workflows.
-   `dataproviders/`: Contains concrete implementations for the interfaces defined in `core/interfaces`. It handles all interactions with external data sources like APIs and files.
-   `entrypoints/`: Contains the entry point of the application (`run_etl.py`) which initializes and runs the ETL process.
-   `config/`: Contains configuration files for the application.
-   `tests/`: (Future placeholder) Will contain tests for the application.

## How to Run

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure the pipeline:**

    Open `config/pipeline.conf` and add your YouTube API key:

    ```ini
    [youtube_api]
    api_key = YOUR_API_KEY
    region_code = PL

    [data]
    output_path = youtube_trends.csv
    ```

3.  **Run the ETL process:**

    ```bash
    python entrypoints/run_etl.py
    ```

    The output will be saved to the file specified by `output_path` in the configuration (e.g., `youtube_trends.csv`).
