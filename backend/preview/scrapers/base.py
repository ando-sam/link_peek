import os
import httpx
from html.parser import HTMLParser

APIFY_PROXY_TOKEN = os.environ.get("APIFY_PROXY_TOKEN")
APIFY_PROXY_HOST = "http://proxy.apify.com:8000"
DEFAULT_TIMEOUT = 10
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


class ScrapeError(Exception):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class BaseScraper:
    def __init__(self, url: str):
        self.url = url

    def fetch_preview(self) -> dict:
        raise NotImplementedError

    def call_apify_actor(self, actor_id: str, payload: dict) -> dict:
        token = os.environ.get("APIFY_TOKEN")
        if not token:
            raise ScrapeError("Apify token is not configured.", status_code=503)

        runs_url = f"https://api.apify.com/v2/acts/{actor_id}/runs"
        params = {"token": token, "waitForFinish": 60}

        try:
            with httpx.Client(timeout=DEFAULT_TIMEOUT, headers=DEFAULT_HEADERS) as client:
                response = client.post(runs_url, params=params, json=payload)
                response.raise_for_status()
                run_payload = response.json()
        except httpx.RequestError as exc:
            raise ScrapeError("Unable to reach Apify.", status_code=503) from exc
        except httpx.HTTPStatusError as exc:
            raise ScrapeError("Apify returned an error while starting the actor.", status_code=502) from exc
        except ValueError as exc:
            raise ScrapeError("Unable to parse Apify response.", status_code=502) from exc

        run_data = run_payload.get("data", run_payload)
        status = str(run_data.get("status", "")).upper()
        if status and status != "SUCCEEDED":
            raise ScrapeError("Apify actor did not complete successfully.", status_code=503)

        output = run_data.get("output")
        if isinstance(output, dict) and output:
            return output
        if isinstance(output, list) and output:
            first_item = output[0]
            if isinstance(first_item, dict):
                return first_item

        dataset_id = run_data.get("defaultDatasetId")
        if not dataset_id:
            return run_data if isinstance(run_data, dict) else {}

        dataset_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items"
        try:
            with httpx.Client(timeout=DEFAULT_TIMEOUT, headers=DEFAULT_HEADERS) as client:
                response = client.get(
                    dataset_url,
                    params={"token": token, "clean": "true", "format": "json"},
                )
                response.raise_for_status()
                dataset_items = response.json()
        except httpx.RequestError as exc:
            raise ScrapeError("Unable to reach Apify dataset results.", status_code=503) from exc
        except httpx.HTTPStatusError as exc:
            raise ScrapeError("Apify returned an error while reading dataset results.", status_code=502) from exc
        except ValueError as exc:
            raise ScrapeError("Unable to parse Apify dataset results.", status_code=502) from exc

        if isinstance(dataset_items, dict):
            return dataset_items
        if isinstance(dataset_items, list) and dataset_items:
            first_item = dataset_items[0]
            if isinstance(first_item, dict):
                return first_item

        raise ScrapeError("Apify returned no preview data.", status_code=502)

    def get_html(self, url: str) -> str:
        target_url = url
        request_params = {}

        if APIFY_PROXY_TOKEN:
            target_url = APIFY_PROXY_HOST
            request_params = {"token": APIFY_PROXY_TOKEN, "url": url}

        try:
            response = httpx.get(
                target_url,
                headers=DEFAULT_HEADERS,
                params=request_params,
                timeout=DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            return response.text
        except httpx.RequestError as exc:
            raise ScrapeError("Unable to reach the remote host.") from exc
        except httpx.HTTPStatusError as exc:
            raise ScrapeError(
                "Remote host returned an unexpected status code.", status_code=502
            ) from exc

    class _MetaParser(HTMLParser):
        def __init__(self, target_key: str):
            super().__init__()
            self.target_key = target_key
            self.found: str | None = None

        def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
            if self.found is not None:
                return
            if tag.lower() != "meta":
                return

            attrs_dict = {
                name.lower(): value for name, value in attrs if value is not None
            }
            content = attrs_dict.get("content")
            if not content:
                return

            if (
                attrs_dict.get("property") == self.target_key
                or attrs_dict.get("name") == self.target_key
            ):
                self.found = content.strip()

    def get_meta(self, html: str, key: str) -> str | None:
        parser = self._MetaParser(key)
        parser.feed(html)
        return parser.found

    def normalize_fields(self, data: dict) -> dict:
        keys = [
            "url",
            "platform",
            "title",
            "description",
            "image",
            "author",
            "author_url",
            "embed_html",
            "video_url",
            "thumbnail_url",
        ]
        return {key: data.get(key) or None for key in keys}
