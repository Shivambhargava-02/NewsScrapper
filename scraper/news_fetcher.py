import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime


# ─────────────────────────────────────────────
#  NewsAPI fetcher
# ─────────────────────────────────────────────
def fetch_newsapi(query: str, api_key: str, page_size: int = 20) -> list[dict]:
    """Fetch articles from NewsAPI /v2/everything endpoint."""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "apiKey": api_key,
        "pageSize": page_size,
        "sortBy": "publishedAt",
        "language": "en",
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("status") != "ok":
            return []

        articles = []
        for art in data.get("articles", []):
            articles.append({
                "title":       art.get("title", "No Title"),
                "source":      art.get("source", {}).get("name", "Unknown"),
                "description": art.get("description") or "No description available.",
                "url":         art.get("url", "#"),
                "image":       art.get("urlToImage", ""),
                "published":   _format_date(art.get("publishedAt", "")),
            })
        return articles
    except Exception:
        return []


# ─────────────────────────────────────────────
#  BeautifulSoup / RSS fallback
# ─────────────────────────────────────────────
def fetch_rss_scrape(query: str, max_results: int = 20) -> list[dict]:
    """
    Scrape Google News RSS feed for a given query.
    No API key required.
    """
    query_encoded = query.replace(" ", "+")
    rss_url = f"https://news.google.com/rss/search?q={query_encoded}&hl=en-IN&gl=IN&ceid=IN:en"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    try:
        resp = requests.get(rss_url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.content, "lxml-xml")  # lxml XML parser for RSS
        items = soup.find_all("item")[:max_results]

        articles = []
        for item in items:
            title_tag   = item.find("title")
            link_tag    = item.find("link")
            source_tag  = item.find("source")
            pub_tag     = item.find("pubDate")
            desc_tag    = item.find("description")

            source = source_tag.get_text(strip=True) if source_tag else "Google News"

            # Google News RSS titles end with "- Source Name"; strip that suffix
            raw_title = title_tag.get_text(strip=True) if title_tag else "No Title"
            title = raw_title.rsplit(" - ", 1)[0].strip() if " - " in raw_title else raw_title

            link = link_tag.get_text(strip=True) if link_tag else "#"
            pub  = _format_date(pub_tag.get_text(strip=True)) if pub_tag else "Unknown date"

            # Description in Google News RSS is wrapped in HTML — parse it properly
            desc = "No description available."
            if desc_tag:
                # The description content is CDATA / HTML — parse it with html.parser
                raw_html = str(desc_tag)
                inner_soup = BeautifulSoup(raw_html, "html.parser")
                # Extract only plain text, skip any nested links/tags
                plain_text = inner_soup.get_text(separator=" ", strip=True)
                # Remove the trailing duplicate title that Google sometimes adds
                plain_text = plain_text.strip()
                desc = plain_text[:280] + ("…" if len(plain_text) > 280 else "")

            articles.append({
                "title":       title,
                "source":      source,
                "description": desc,
                "url":         link,
                "image":       "",  # RSS feed doesn't reliably carry images
                "published":   pub,
            })
        return articles
    except Exception as e:
        return []


# ─────────────────────────────────────────────
#  Unified entry point
# ─────────────────────────────────────────────
def get_news(query: str, api_key: str | None = None, page_size: int = 20) -> tuple[list[dict], str]:
    """
    Returns (articles, source_label).
    Tries NewsAPI first; falls back to BeautifulSoup RSS scraping.
    """
    key = api_key or os.getenv("NEWS_API_KEY", "")
    if key and key != "your_newsapi_key_here":
        articles = fetch_newsapi(query, key, page_size)
        if articles:
            return articles, "NewsAPI"

    # Fallback
    articles = fetch_rss_scrape(query, page_size)
    return articles, "Google News RSS (BeautifulSoup)"


# ─────────────────────────────────────────────
#  Utility
# ─────────────────────────────────────────────
def _format_date(raw: str) -> str:
    """Try to parse and pretty-print a date string."""
    formats = [
        "%Y-%m-%dT%H:%M:%SZ",
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S GMT",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(raw.strip(), fmt)
            return dt.strftime("%b %d, %Y  %I:%M %p")
        except ValueError:
            continue
    return raw.strip() or "Unknown date"
