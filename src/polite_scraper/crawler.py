from bs4 import BeautifulSoup

from polite_scraper.config import BASE_URL, PAGE_COUNT
from polite_scraper.fetcher import fetch_page
from polite_scraper.parser import book_links, next_page_url


def collect_urls() -> dict[str, str]:
    """Map each book detail URL to the catalogue page it was found on."""
    collected: dict[str, str] = {}
    page_url: str | None = BASE_URL
    catalogue_pages = 0

    while page_url is not None and catalogue_pages < PAGE_COUNT:
        soup = BeautifulSoup(fetch_page(page_url), "html.parser")
        for link in book_links(soup, page_url):
            collected.setdefault(link, page_url)  # keep earliest source page
        catalogue_pages += 1
        page_url = next_page_url(soup, page_url) if catalogue_pages < PAGE_COUNT else None

    print(f"detail_pages={len(collected)}")
    return collected