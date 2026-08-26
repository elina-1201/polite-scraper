
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from datetime import datetime

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

def raw_record(soup: BeautifulSoup, product_url: str, source_page: str) -> dict:
    """Extract a raw record from an already-fetched detail page soup (pure, no I/O)."""
    product_main = soup.select_one("div.col-sm-6.product_main")

    title = product_main.select_one("h1").text.strip()
    price_text = product_main.select_one("p.price_color").text.strip()
    availability = product_main.select_one("p.availability").text.strip()
    rating = product_main.select_one("p.star-rating")["class"][1]
    description_el = soup.select_one("div#product_description + p")
    description = description_el.text.strip() if description_el else None

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability,
        "rating_text": rating,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now().isoformat(),
    }