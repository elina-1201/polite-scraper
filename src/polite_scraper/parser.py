
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime

from polite_scraper.fetcher import fetch_page


def book_links(soup: BeautifulSoup, page_url: str) -> list[str]:
    links: list[str] = []
    for article in soup.select("article.product_pod"):
        link = article.select_one("h3 a")
        if link is None:
            continue
        links.append(urljoin(page_url, link["href"]))
    return links


def next_page_url(soup: BeautifulSoup, page_url: str) -> str | None:
    link = soup.select_one("li.next a")
    if link is None:
        return None
    return urljoin(page_url, link["href"])

def print_record(item_url: str, source_page: str | None = None) -> None:
    detail_page = BeautifulSoup(fetch_page(item_url), "html.parser")
    product_main = detail_page.select_one("div.col-sm-6.product_main")
    title = product_main.select_one("h1").text.strip()
    product_url = item_url
    price = product_main.select_one("p.price_color").text.strip()
    availability = product_main.select_one("p.availability").text.strip()
    rating = product_main.select_one("p.star-rating")["class"][1]
    description_el = detail_page.select_one("div#product_description + p")
    decscription = description_el.text.strip() if description_el else None
    fetched_at = datetime.now()

    record = {
        "title": title,
        "product_url": product_url,
        "price_text": price,
        "availability_text": availability,
        "rating_text": rating,
        "description": decscription,
        "source_page": source_page,
        "fetched_at": fetched_at.isoformat(),
    }

    # print(product_main)
    print(record)