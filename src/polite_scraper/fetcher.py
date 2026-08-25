import requests

from polite_scraper.config import BASE_URL, CACHE_DIR, TIMEOUT, USER_AGENT


def fetch_page(page: int = 1) -> str:
    output = CACHE_DIR / f"catalogue-page-{page}.html"

    if output.exists():
        print("CACHE HIT")
        return output.read_text(encoding="utf-8")

    print("FETCH")
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT

    response = session.get(BASE_URL, timeout=TIMEOUT)
    response.raise_for_status()

    html = response.text

    # Create the cache folder if it doesn't exist, then save the HTML.
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(f"Saved {output}")

    return html