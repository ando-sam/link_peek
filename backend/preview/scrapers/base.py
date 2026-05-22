import httpx
from bs4 import BeautifulSoup

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

    def get_html(self, url: str) -> str:
        try:
            response = httpx.get(url, headers=DEFAULT_HEADERS, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as exc:
            raise ScrapeError("Unable to reach the remote host.") from exc
        except httpx.HTTPStatusError as exc:
            raise ScrapeError(
                "Remote host returned an unexpected status code.", status_code=502
            ) from exc

    def get_soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "lxml")

    def get_meta(self, soup: BeautifulSoup, key: str) -> str | None:
        tag = soup.find("meta", property=key) or soup.find("meta", attrs={"name": key})
        if tag and tag.get("content"):
            return tag["content"].strip()
        return None

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
