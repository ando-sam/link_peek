import httpx
from .base import BaseScraper, DEFAULT_HEADERS, DEFAULT_TIMEOUT, ScrapeError


class TikTokScraper(BaseScraper):
    PLATFORM = "tiktok"
    OEMBED_URL = "https://www.tiktok.com/oembed"

    def fetch_preview(self) -> dict:
        try:
            response = httpx.get(
                self.OEMBED_URL,
                headers=DEFAULT_HEADERS,
                params={"url": self.url},
                timeout=DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()
        except httpx.RequestError as exc:
            raise ScrapeError("Unable to reach TikTok for preview metadata.") from exc
        except httpx.HTTPStatusError as exc:
            raise ScrapeError(
                "TikTok returned an error while fetching preview.", status_code=502
            ) from exc
        except ValueError as exc:
            raise ScrapeError(
                "Unable to parse TikTok preview metadata.", status_code=502
            ) from exc

        return self.normalize_fields(
            {
                "url": self.url,
                "platform": self.PLATFORM,
                "title": data.get("title"),
                "description": None,
                "image": data.get("thumbnail_url"),
                "author": data.get("author_name"),
                "author_url": data.get("author_url"),
                "embed_html": data.get("html"),
                "video_url": None,
                "thumbnail_url": data.get("thumbnail_url"),
            }
        )
