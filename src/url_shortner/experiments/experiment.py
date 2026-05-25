import requests
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from url_shortner.api.routes import GenerateResponse


def generate_url_list(list_length: float):
    url_list = [f"http://google.com/{i}" for i in range(int(list_length))]
    print("URL_LIST successfully initialized")
    return url_list


def generate_url_ids(url_list: list[str]):
    backend_url = "http://localhost:8000"
    for url in url_list:
        response = requests.post(f"{backend_url}/generate?original_url={url}")
        response_decoded: GenerateResponse = response.json()
        if response_decoded["collisions"] != 0:
            print(
                f"Generated URL_ID for {url}: {response_decoded['url_id']}, collisions: {response_decoded['collisions']}"
            )


if __name__ == "__main__":
    start = time.perf_counter()
    url_list = generate_url_list(1 * 10**4)
    elapsed = time.perf_counter() - start
    print(f"Took {elapsed:.3f}s to generate {len(url_list)} URLs")

    start = time.perf_counter()
    generate_url_ids(url_list)
    elapsed = time.perf_counter() - start
    print(
        f"Took {elapsed:.3f}s to generate {len(url_list)} URL_IDs and insert them in DB"
    )
    start = time.perf_counter()
    response = requests.get("http://localhost:8000/HUfd69X1")
    print(response.status_code)
    elapsed = time.perf_counter() - start
    print(
        f"Took {elapsed:.3f}s to retrieve an arbitrary original_ID. Number of rows in DB is approx 2.7 mil"
    )
