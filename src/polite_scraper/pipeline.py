# pipeline.py
import time
from datetime import datetime
from polite_scraper.crawler import collect_urls
from polite_scraper.fetcher import fetch_page, get_stats, reset_stats
from polite_scraper.models import RunResult, RunSummary
from polite_scraper.parser import raw_record
from polite_scraper.storage import *
from polite_scraper.validator import validate_record

def log_entry(url, source, error) -> dict:
    return {"url": url, "source": source, "error": error,
            "fetched_at": datetime.now().isoformat()}

def _process(url: str, source: str) -> tuple[dict | None, dict | None]:
    soup = fetch_page(url)
    raw = raw_record(soup, url, source)
    return validate_record(raw)

def run_pipeline() -> RunResult:
    reset_stats()
    urls = collect_urls()
    result = RunResult()

    start = time.monotonic()
    start_point = datetime.now().isoformat()

    for url, source in urls.items():
        try:
            book, error = _process(url, source)
        except Exception as e:
            result.logs.append(log_entry(url, source, str(e)))
            continue
        if book:
            result.books.append(book)
        if error:
            result.errors.append(error)

    write_books(result.books)
    write_errors(result.errors)
    write_logs(result.logs)

    stats = get_stats()
    result.summary = RunSummary(
        start_time=start_point,
        duration=time.monotonic() - start,
        pages_fetched=stats["pages_fetched"],
        cache_hits=stats["cache_hits"],
        valid_records=len(result.books),
        invalid_records=len(result.errors),
        failed_pages=len(result.logs),
    )
    write_reports([build_report(result.summary)])
    return result
