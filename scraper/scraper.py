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
                "link": link,
                "published": published,
                "summary": summary_short,
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


def get_news(query, api_key, page_size=10):

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": query,
        "pageSize": page_size,
        "apiKey": api_key,
        "language": "en",
        "sortBy": "publishedAt"
    }

    response = requests.get(url, params=params)
    data = response.json()

    articles = data.get("articles", [])

    return articles, "NewsAPI"

def get_news(query, api_key, page_size=10):
    
    articles = fetch_bbc_india_news(query)

    source_label = "BBC India"

    return articles, source_label