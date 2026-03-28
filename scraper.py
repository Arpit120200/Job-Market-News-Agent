import requests
import feedparser
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def scrape_rss_feed(feed_url, source_name, max_entries=8):
    """
    Parses an RSS feed with a timeout to prevent hanging.
    """
    try:
        # Fetch the raw feed content ourselves with a timeout
        # then pass it to feedparser to parse
        response = requests.get(feed_url, headers=HEADERS, timeout=8)
        response.raise_for_status()

        feed = feedparser.parse(response.content)

        if not feed.entries:
            print(f"  No entries found in feed")
            return ""

        content = f"Latest from {source_name}:\n"
        for entry in feed.entries[:max_entries]:
            title = entry.get("title", "").strip()
            summary = entry.get("summary", "").strip()

            if summary:
                soup = BeautifulSoup(summary, "html.parser")
                summary = soup.get_text(strip=True)[:300]

            if title:
                content += f"\n- {title}"
                if summary:
                    content += f": {summary}"

        return content

    except Exception as e:
        print(f"  Could not parse feed from {source_name}: {e}")
        return ""


def scrape_url(url, source_name):
    """
    Falls back to direct HTML scraping for sites
    that do not have RSS feeds.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text(strip=True) for p in paragraphs)
        return text[:3000] if text else ""

    except Exception as e:
        print(f"  Could not scrape {source_name}: {e}")
        return ""


def collect_job_market_data():
    """
    Collects job market data from multiple reliable sources
    using RSS feeds and direct scraping.
    """

    # RSS feed sources — these are reliable and scraper friendly
    rss_sources = {
    "TechCrunch — Layoffs": "https://techcrunch.com/tag/layoffs/feed/",
    "TechCrunch — Jobs": "https://techcrunch.com/tag/jobs/feed/",
    "BBC — Business News": "http://feeds.bbci.co.uk/news/business/rss.xml",
    "CNBC — Economy": "https://www.cnbc.com/id/20910258/device/rss/rss.html",
    "CNBC — Tech": "https://www.cnbc.com/id/19854910/device/rss/rss.html",
    "Harvard Business Review": "http://feeds.hbr.org/harvardbusiness",
    "Hacker News — Who is Hiring": "https://hnrss.org/ask?q=who+is+hiring",
    "WSJ — Economy": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
    "Glassdoor Blog": "https://www.glassdoor.com/blog/feed/",
    "GitHub Blog": "https://github.blog/feed/",
    "Y Combinator News": "https://news.ycombinator.com/rss",
    "Stack Overflow Blog": "https://stackoverflow.blog/feed/"
    }

    direct_sources = {
    "Layoffs.fyi": "https://layoffs.fyi",
    "Levels.fyi Blog": "https://www.levels.fyi/blog/"
    }

    collected = {}
    today = datetime.now().strftime("%B %d, %Y")

    print(f"  Collecting data for {today}")

    # Collect from RSS feeds
    for source_name, feed_url in rss_sources.items():
        print(f"  Fetching {source_name}...")
        content = scrape_rss_feed(feed_url, source_name)
        if content and len(content) > 50:
            collected[source_name] = content
            print(f"  Got {len(content)} characters")
        else:
            print(f"  Skipped — insufficient content")

    # Collect from direct scrape sources
    for source_name, url in direct_sources.items():
        print(f"  Scraping {source_name}...")
        content = scrape_url(url, source_name)
        if content and len(content) > 50:
            collected[source_name] = content
            print(f"  Got {len(content)} characters")
        else:
            print(f"  Skipped — insufficient content")

    print(f"\n  Successfully collected from {len(collected)} sources")
    return collected