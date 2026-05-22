from urllib.parse import urlparse

SUPPORTED_DOMAINS = {
    "facebook.com": "facebook",
    "www.facebook.com": "facebook",
    "m.facebook.com": "facebook",
    "instagram.com": "instagram",
    "www.instagram.com": "instagram",
    "tiktok.com": "tiktok",
    "www.tiktok.com": "tiktok",
}


def normalize_url(raw_url: str) -> str:
    parsed = urlparse(raw_url)
    if not parsed.scheme:
        parsed = urlparse(f"https://{raw_url}")
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must use http or https.")
    if not parsed.netloc:
        raise ValueError("URL is not valid.")
    return parsed.geturl()


def validate_social_url(raw_url: str) -> str:
    normalized = normalize_url(raw_url)
    domain = urlparse(normalized).netloc.lower()
    if domain.endswith(":80") or domain.endswith(":443"):
        domain = domain.rsplit(":", 1)[0]
    if domain not in SUPPORTED_DOMAINS:
        raise ValueError(
            "Unsupported URL. Only Facebook, Instagram, and TikTok links are accepted."
        )
    return normalized


def detect_platform_from_url(raw_url: str) -> str:
    domain = urlparse(raw_url).netloc.lower()
    if domain.endswith(":80") or domain.endswith(":443"):
        domain = domain.rsplit(":", 1)[0]
    return SUPPORTED_DOMAINS.get(domain, "")
