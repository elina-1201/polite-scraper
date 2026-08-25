import time
from pathlib import Path
from urllib.parse import urlparse

import requests

from polite_scraper.config import BASE_URL, CACHE_DIR, DELAY_SECONDS, TIMEOUT, USER_AGENT

# Time of the last real HTTP request, used to space requests out politely.
_last_request_time = 0.0


def _cache_path_for(url: str) -> Path:
    """Map a catalogue URL to its local cache file."""
    path = urlparse(url).path
    if path in ("", "/"):
        return CACHE_DIR / "catalogue-page-1.html"

    # e.g. /catalogue/page-2.html -> catalogue-page-2.html
    filename = Path(path).name
    return CACHE_DIR / f"catalogue-{filename}"


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


def fetch_page(url: str = BASE_URL) -> str:
    output = _cache_path_for(url)

    if output.exists():
        print(f"CACHE HIT {output}")
        return output.read_text(encoding="utf-8")

    print(f"FETCH {url}")
    _politeness_delay()

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()

    html = response.text

    # Create the cache folder if it doesn't exist, then save the HTML.
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(f"Saved {output}")

    return html