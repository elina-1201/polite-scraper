import time
import hashlib
import requests

from polite_scraper.config import BASE_URL, CACHED_ITEMS_DIR, CACHED_PAGES_DIR, DELAY_SECONDS, MAX_RETRIES, RETRY_DELAY_SECONDS, TIMEOUT, USER_AGENT
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup


# Time of the last real HTTP request, used to space requests out.
_last_request_time = 0.0
_fetch_attempts = 0
_cache_hits = 0


def reset_stats() -> None:
    """Zero out the fetch/cache counters before a run."""
    global _fetch_attempts, _cache_hits
    _fetch_attempts = 0
    _cache_hits = 0


def get_stats() -> dict:
    """Return the accumulated fetch/cache counters for the run."""
    return {"pages_fetched": _fetch_attempts, "cache_hits": _cache_hits}


def fetch_page(url: str = BASE_URL) -> BeautifulSoup:
    global _fetch_attempts, _cache_hits
    
    output = _cache_path_for(url)

    if output.exists():
        _cache_hits += 1
        return BeautifulSoup(output.read_text(encoding="utf-8"), "html.parser")

    print(f"FETCH {url}")
    _politeness_delay()
    _fetch_attempts += 1

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    response = _get_with_retry(session, url)
    
    response.encoding = "utf-8"
    html = response.text

    # Create the cache folder if it doesn't exist, then save the HTML.
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(f"Saved {output}")

    return BeautifulSoup(html, "html.parser")


def _get_with_retry(session: requests.Session, url: str) -> requests.Response:
    """Return the HTTP response, retrying once on transient failures.

    Retries only timeouts, connection errors, and 5xx responses.
    4xx (e.g. 404, 403) are re-raised immediately and never retried.
    """
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return response

        except requests.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None
            if status is not None and _is_retryable_status(status) and attempt < MAX_RETRIES:
                print(f"HTTP {status} for {url}; retrying...")
                time.sleep(RETRY_DELAY_SECONDS)
                continue
            raise

        except (requests.Timeout, requests.ConnectionError):
            if attempt < MAX_RETRIES:
                print(f"Network error for {url}; retrying...")
                time.sleep(RETRY_DELAY_SECONDS)
                continue
            raise

def _is_retryable_status(status: int) -> bool:
    return 500 <= status < 600


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