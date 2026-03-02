"""dlt REST API pipeline for NYC taxi data."""

import dlt
from dlt.sources.rest_api import rest_api_source
from dlt.sources.rest_api.typing import RESTAPIConfig


def build_taxi_source() -> dlt.sources.DltSource:
    """Configure REST API source for the NYC taxi data."""
    config: RESTAPIConfig = {
        "client": {
            # Base URL of the Zoomcamp Cloud Function API, as requested
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api",
        },
        "resources": [
            {
                "name": "nyc_taxi_trips",
                "endpoint": {
                    # Path is empty because base_url already points at the function
                    "path": "",
                    # Use offset-based pagination with 1,000 rows per page.
                    # Limit ingestion to the first 10 pages (10,000 rows).
                    # The API returns an empty list [] when there is no more data,
                    # so we rely on `stop_after_empty_page=True` as a safety net.
                    "paginator": {
                        "type": "offset",
                        # Explicitly disable `total` expectation so the paginator
                        # can rely on empty pages to stop.
                        "total_path": None,
                        "limit": 1000,
                        "offset": 0,
                        "offset_param": "offset",
                        "limit_param": "limit",
                        # With limit=1000, this caps ingestion at 10 pages.
                        "maximum_offset": 10000,
                        "stop_after_empty_page": True,
                    },
                },
            },
        ],
    }

    return rest_api_source(config)


def taxi_pipeline() -> None:
    """Run the taxi pipeline end-to-end."""
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="nyc_taxi_data",
        progress="log",
        # For development: start from a clean state on each run.
        # Remove `refresh` when you want to accumulate data incrementally.
        refresh="drop_sources",
    )

    source = build_taxi_source()
    load_info = pipeline.run(source)
    print(load_info)  # noqa: T201


if __name__ == "__main__":
    taxi_pipeline()

