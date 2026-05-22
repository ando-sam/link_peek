from urllib.parse import urlparse

from .facebook import FacebookScraper
from .instagram import InstagramScraper
from .tiktok import TikTokScraper
from ..validators import SUPPORTED_DOMAINS


class UnsupportedPlatformError(ValueError):
    pass


def get_scraper_for_url(raw_url: str):
    parsed = urlparse(raw_url)
    domain = parsed.netloc.lower()
    if domain.endswith(":80") or domain.endswith(":443"):
        domain = domain.rsplit(":", 1)[0]

    platform = SUPPORTED_DOMAINS.get(domain)
    if not platform:
        raise UnsupportedPlatformError(
            "Unsupported URL. Only Facebook, Instagram, and TikTok links are accepted."
        )

    if platform == "facebook":
        return FacebookScraper(raw_url)
    if platform == "instagram":
        return InstagramScraper(raw_url)
    if platform == "tiktok":
        return TikTokScraper(raw_url)

    raise UnsupportedPlatformError(
        "Unsupported URL. Only Facebook, Instagram, and TikTok links are accepted."
    )
