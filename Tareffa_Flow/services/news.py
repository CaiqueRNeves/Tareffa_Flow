from __future__ import annotations
import feedparser
from dataclasses import dataclass
from typing import List


@dataclass
class NewsItem:
    title: str
    link: str
    source: str
    summary: str | None
    image: str | None


FEEDS = {
    "Hacker News": "https://news.ycombinator.com/rss",
    "The Verge": "https://www.theverge.com/rss/index.xml",
    "Dev.to": "https://dev.to/feed",
}


def _first_image(entry) -> str | None:
    media = entry.get("media_thumbnail") or entry.get("media_content")
    if media and isinstance(media, list) and media[0].get("url"):
        return media[0]["url"]
    html = entry.get("summary") or entry.get("summary_detail", {}).get("value") or ""
    for token in ['src="', "src='"]:
        i = html.find(token)
        if i != -1:
            j = html.find('"' if token == 'src="' else "'", i + len(token))
            if j != -1:
                return html[i + len(token) : j]
    return None


def fetch_news(limit_total: int = 6) -> List[NewsItem]:
    items: List[NewsItem] = []
    per_feed = max(2, limit_total // len(FEEDS))
    for source, url in FEEDS.items():
        parsed = feedparser.parse(url)
        for entry in parsed.entries[:per_feed]:
            items.append(
                NewsItem(
                    title=entry.get("title", "(sem título)"),
                    link=entry.get("link", "#"),
                    source=source,
                    summary=(entry.get("summary") or entry.get("description") or None),
                    image=_first_image(entry),
                )
            )
    return items[:limit_total]
