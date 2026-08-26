from polite_scraper.crawler import collect_urls
from polite_scraper.fetcher import fetch_page
from polite_scraper.parser import raw_record
from polite_scraper.sotrage import write_books, write_errors
from polite_scraper.validator import validate_record

def build_record(url: str, source: str) -> tuple[dict | None, dict | None]:
    soup = fetch_page(url)
    raw = raw_record(soup, url, source)
    return validate_record(raw)

def main() -> None:
    urls = collect_urls()
    books: list[dict] = []
    errors: list[dict] = []

    for url, source in urls.items():
        book, error = build_record(url, source)
        if book:
            books.append(book)
        if error:
            errors.append(error)

    write_books(books)
    write_errors(errors)

    print(f"books={len(books)} errors={len(errors)}")  