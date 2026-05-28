import os
import httpx
from .base import BaseScraper, DEFAULT_HEADERS, DEFAULT_TIMEOUT, ScrapeError


class TikTokScraper(BaseScraper):
    PLATFORM = "tiktok"
    OEMBED_URL = "https://www.tiktok.com/oembed"

    def get_apify_actor_id(self):
        # Try platform-specific env var first, then fall back to generic
        return os.environ.get("APIFY_TIKTOK_ACTOR_ID", "")

    def normalize_apify_data(self, apify_data: dict) -> dict:
        """
        Normalize Apify actor output for TikTok to our standard preview format.
        This mapping will depend on what the specific Apify actor returns.
        """
        # Default mapping - adjust based on actual Apify actor output
        return {
            "url": apify_data.get("url", self.url),
            "platform": self.PLATFORM,
            "title": apify_data.get("title"),
            "description": apify_data.get("description"),
            "image": apify_data.get("image"),
            "author": apify_data.get("author_name") or apify_data.get("author"),
            "author_url": apify_data.get("author_url"),
            "embed_html": apify_data.get("html"),  # Apify might return HTML embed
            "video_url": apify_data.get("video_url"),
            "thumbnail_url": apify_data.get("thumbnail_url"),
        }

    def fetch_preview(self) -> dict:
        # Try Apify first if configured
        if os.environ.get("APIFY_TOKEN") and self.get_apify_actor_id():
            try:
                apify_input = {
                    "url": self.url,
                    # Add any other parameters the Apify actor expects
                }
                apify_result = self.call_apify_actor(self.get_apify_actor_id(), apify_input)
                normalized = self.normalize_apify_data(apify_result)
                return self.normalize_fields(normalized)
            except Exception as e:
                # Fall back to direct scraping if Apify fails
                pass

        # Fallback to direct oEmbed request (original implementation)
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
                "description": None,  # TikTok oEmbed doesn't provide description
                "image": data.get("thumbnail_url"),
                "author": data.get("author_name"),
                "author_url": data.get("author_url"),
                "embed_html": data.get("html"),
                "video_url": None,
                "thumbnail_url": data.get("thumbnail_url"),
            }
        )