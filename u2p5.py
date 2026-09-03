from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import requests


LOG_FILE = Path("app.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def setup_directories() -> Path:
    """Ensure the data directory exists."""
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def fetch_api_data(url: str) -> tuple[dict | list | None, int]:
    """Retrieve data from the specified API URL and handle HTTP errors."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        status = (
            response.status_code if "response" in locals() else 500
        )  # Fallback
        return None, status
    except requests.exceptions.RequestException as err:
        print(f"An error occurred during the request: {err}")
        return None, 0


def process_data(data: dict | list) -> list[dict]:
    
    #Normalize Input To a List of Items
    items = data if isinstance(data, list) else [data]
    processed_records = []

    for item in items:
        #Extract Fields Dynamically or Fall Back Gracefully
        record = {
            "id": item.get("id"),
            "title": item.get("title") or item.get("name") or "N/A",
            "content": item.get("body")
            or item.get("description")
            or str(item),
        }
        processed_records.append(record)

    return processed_records


def log_application_state(
    url: str, status_code: int, records_count: int, status: str
) -> None:
    request_time = datetime.now(timezone.utc).isoformat()
    log_message = (
        f"Request Time : {request_time} | "
        f"API URL : {url} | "
        f"Status Code : {status_code} | "
        f"Records Received : {records_count} | "
        f"Processing Status : {status}"
    )
    logging.info(log_message)


def main():
    data_dir = setup_directories()

    #Prompt User For Input
    default_url = "https://jsonplaceholder.typicode.com/posts"
    user_url = input(f"Enter API URL (Press Enter For Default: {default_url}): ").strip()
    url = user_url if user_url else default_url

    print(f"\nFetching Data From {url}...")
    raw_data, status_code = fetch_api_data(url)

    if raw_data is None:
        print("Failed To Fetch or Parse API Response.")
        log_application_state(url, status_code, 0, "FAILED_FETCH")
        return

    #Determine Total Records Received
    records_count = len(raw_data) if isinstance(raw_data, list) else 1

    #Save Raw API Response
    raw_path = data_dir / "raw.json"
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2)
    print(f"Raw Data Saved to {raw_path}")

    #Process And Filter Fields For AI Context Building
    processed_data = process_data(raw_data)

    #Save Processed Data
    processed_path = data_dir / "processed.json"
    with open(processed_path, "w", encoding="utf-8") as f:
        json.dump(processed_data, f, indent=2)
        
    print(f"Processed Data Saved To {processed_path}")

    #Log Successful Execution
    log_application_state(url, status_code, records_count, "SUCCESS")
    print("Execution Finished Successfully. Logs Updated In app.log.")


if __name__ == "__main__":
    main()