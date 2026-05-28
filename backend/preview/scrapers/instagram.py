import os
from .base import BaseScraper


class InstagramScraper(BaseScraper):
    PLATFORM = "instagram"

    def get_apify_actor_id(self):
        # Try platform-specific env var first, then fall back to generic
        return os.environ.get("APIFY_INSTAGRAM_ACTOR_ID", "")

    def normalize_apify_data(self, apify_data: dict) -> dict:
        """
        Normalize Apify actor output for Instagram to our standard preview format.
        This mapping will depend on what the specific Apify actor returns.
        """
        # Default mapping - adjust based on actual Apify actor output
        return {
            "url": apify_data.get("url", self.url),
            "platform": self.PLATFORM,
            "title": apify_data.get("title") or apify_data.get("og:title"),
            "description": apify_data.get("description") or apify_data.get("og:description"),
            "image": apify_data.get("image") or apify_data.get("og:image"),
            "author": apify_data.get("author") or apify_data.get("og:site_name"),
            "author_url": apify_data.get("author_url") or apify_data.get("og:url"),
            "embed_html": apify_data.get("embed_html") or apify_data.get("og:video"),
            "video_url": apify_data.get("video_url"),
            "thumbnail_url": apify_data.get("thumbnail_url") or apify_data.get("og:image"),
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

        # Fallback to direct scraping (original implementation)
        html = self.get_html(self.url)
        title = self.get_meta(html, "og:title")
        description = self.get_meta(html, "og:description")
        image = self.get_meta(html, "og:image")
        author = self.get_meta(html, "og:site_name") or self.get_meta(html, "author")
        author_url = self.get_meta(html, "og:url")
        embed_html = self.get_meta(html, "og:video")
        thumbnail_url = self.get_meta(html, "og:image")
        return self.normalize_fields(
            {
                "url": self.url,
                "platform": self.PLATFORM,
                "title": title,
                "description": description,
                "image": image,
                "author": author,
                "author_url": author_url,
                "embed_html": embed_html,
                "video_url": None,
                "thumbnail_url": thumbnail_url,
            }
        )