
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from polite_scraper.config import BASE_URL, PAGE_COUNT
from polite_scraper.fetcher import fetch_page


def _book_links(soup: BeautifulSoup, page_url: str) -> list[str]:
    links: list[str] = []
    for article in soup.select("article.product_pod"):
        link = article.select_one("h3 a")
        if link is None:
            continue
        links.append(urljoin(page_url, link["href"]))
    return links


def _next_page_url(soup: BeautifulSoup, page_url: str) -> str | None:
    link = soup.select_one("li.next a")
    if link is None:
        return None
    return urljoin(page_url, link["href"])


def parser() -> list[str]:
    book_links: list[str] = []
    page_url: str | None = BASE_URL
    catalogue_pages = 0
    discovered = 0

    while page_url is not None and catalogue_pages < PAGE_COUNT:
        content = fetch_page(page_url)
        soup = BeautifulSoup(content, "html.parser")

        page_links = _book_links(soup, page_url)
        discovered += len(page_links)
        book_links.extend(page_links)

        catalogue_pages += 1
        page_url = _next_page_url(soup, page_url) if catalogue_pages < PAGE_COUNT else None

    # Drop duplicate book links, keeping the order they first appeared.
    unique_urls = list(dict.fromkeys(book_links))

    print(f"catalogue_pages={catalogue_pages} discovered={discovered} unique_urls={len(unique_urls)}")
    return unique_urls
