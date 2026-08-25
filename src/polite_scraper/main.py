from polite_scraper.crawler import collect_urls
from polite_scraper.fetcher import  fetch_page
from polite_scraper.parser import print_record

def main() -> None:
    urls = collect_urls()
    for item_url, source_page in urls.items():
        print_record(item_url, source_page)
        break