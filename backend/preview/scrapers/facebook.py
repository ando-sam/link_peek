from .base import BaseScraper


class FacebookScraper(BaseScraper):
    PLATFORM = "facebook"

    def fetch_preview(self) -> dict:
        html = self.get_html(self.url)
        soup = self.get_soup(html)
        title = self.get_meta(soup, "og:title") or self.get_meta(soup, "title")
        description = self.get_meta(soup, "og:description") or self.get_meta(
            soup, "description"
        )
        image = self.get_meta(soup, "og:image")
        author = self.get_meta(soup, "og:site_name")
        author_url = self.get_meta(soup, "og:url")
        embed_html = self.get_meta(soup, "og:video") or None
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
                "thumbnail_url": None,
            }
        )
