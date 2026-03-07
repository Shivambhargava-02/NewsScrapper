import requests
import pandas as pd
import feedparser
from io import BytesIO

RSS_URL = "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"

def fetch_bbc_india_news():
    feed = feedparser.parse(RSS_URL)
    items = []
    for entry in feed.entries:
        title = entry.get("title", "").strip()
        link = entry.get("link", "").strip()
        published = entry.get("published", "")
        summary = entry.get("summary", "")
        if summary:
            words = summary.split()
            summary_short = " ".join(words[:40])
        else:
            summary_short = ""
        items.append(
            {
                "title": title,
                "url": link,
                "published": published,
                "description": summary_short,
                "source": "BBC News"
            }
        )
    if not items:
        return pd.DataFrame(columns=["title", "link", "published", "summary"])
    return pd.DataFrame(items)

def dataframe_to_excel(df):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="News")
    buffer.seek(0)
    return buffer



def get_news(query, api_key=None, page_size=10):
    """
    Delegates to news_fetcher.get_news which properly searches
    Google News RSS (or NewsAPI) for the given query/category.
    """
    from scraper.news_fetcher import get_news as _get_news
    return _get_news(query, api_key=api_key, page_size=page_size)
