from .base import BaseScraper


class InstagramScraper(BaseScraper):
    PLATFORM = "instagram"

    def fetch_preview(self) -> dict:
        html = self.get_html(self.url)
        soup = self.get_soup(html)
        title = self.get_meta(soup, "og:title")
        description = self.get_meta(soup, "og:description")
        image = self.get_meta(soup, "og:image")
        author = self.get_meta(soup, "og:site_name") or self.get_meta(soup, "author")
        author_url = self.get_meta(soup, "og:url")
        embed_html = self.get_meta(soup, "og:video")
        thumbnail_url = self.get_meta(soup, "og:image")
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
