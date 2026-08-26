import json

from polite_scraper.config import OUTPUT_DIR
from polite_scraper.models import RunSummary


def write_json(filename: str, data) -> None:
    """Write ``data`` as pretty-printed JSON to ``OUTPUT_DIR / filename``.

    Overwrites any existing file at that path.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / filename).write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def write_books(records: list[dict]) -> None:
    write_json("books.json", records)


def write_errors(errors: list[dict]) -> None:
    write_json("errors.json", errors)


def write_logs(logs: list[dict]) -> None:
    write_json("logs.json", logs)


def write_reports(reports: list[dict]) -> None:
    """Append ``reports`` to the list already stored in ``run-report.json``."""
    report_path = OUTPUT_DIR / "run-report.json"

    # Load existing reports if the file is present, otherwise start fresh
    existing: list[dict] = []
    if report_path.exists():
        try:
            existing = json.loads(report_path.read_text(encoding="utf-8"))
            if not isinstance(existing, list):
                existing = []
        except (json.JSONDecodeError, OSError):
            existing = []

    existing.extend(reports)
    write_json("run-report.json", existing)    


def build_report(summary: RunSummary) -> dict:
    return {
        "start_time": summary.start_time,
        "duration": summary.duration,
        "pages_fetched": summary.pages_fetched,
        "cache_hits": summary.cache_hits,
        "valid_records": summary.valid_records,
        "invalid_records": summary.invalid_records,
        "failed_pages": summary.failed_pages,
    }
