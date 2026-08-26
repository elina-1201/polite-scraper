import time
import hashlib
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import requests

from polite_scraper.config import BASE_URL, CACHED_ITEMS_DIR, CACHED_PAGES_DIR, DELAY_SECONDS, TIMEOUT, USER_AGENT

# Time of the last real HTTP request, used to space requests out politely.
_last_request_time = 0.0


def _cache_path_for(url: str) -> Path:
    """Map a URL to its local cache file.

    Catalogue pages   -> CACHED_PAGES_DIR (e.g. cache/pages/catalogue-page-1.html)
    Book detail pages -> CACHED_ITEMS_DIR (e.g. cache/items/a-light-in-the-attic_1000.html)
    """

    path = urlparse(url).path
    hash = hashlib.md5(url.encode()).hexdigest()[:12]

    # Detail page, e.g. /catalogue/<slug>/index.html
    if path.endswith("/index.html"):
        parts = [p for p in path.split("/") if p]  # ['catalogue', '<slug>', 'index.html']
        slug = parts[-2] if len(parts) >= 2 else hash
        return CACHED_ITEMS_DIR / f"{slug}.html"

    # Catalogue page, e.g. / or /catalogue/page-2.html
    if path in ("", "/"):
        return CACHED_PAGES_DIR / "catalogue-page-1.html"
    return CACHED_PAGES_DIR / f"catalogue-{Path(path).name}"


def _politeness_delay() -> None:
    """Wait at least DELAY_SECONDS (but never under half a second) since the
    last real request. Cached pages never call this, so they add no delay."""
    global _last_request_time

    delay = max(DELAY_SECONDS, 0.5)
    elapsed = time.monotonic() - _last_request_time
    wait = delay - elapsed
    if wait > 0:
        time.sleep(wait)

    _last_request_time = time.monotonic()


def fetch_page(url: str = BASE_URL) -> BeautifulSoup:
    output = _cache_path_for(url)

    if output.exists():
        # print(f"CACHE HIT {output}")
        return BeautifulSoup(output.read_text(encoding="utf-8"), "html.parser")

    print(f"FETCH {url}")
    _politeness_delay()

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    response.encoding = "utf-8"
    html = response.text

    # Create the cache folder if it doesn't exist, then save the HTML.
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(f"Saved {output}")

    return BeautifulSoup(html, "html.parser")