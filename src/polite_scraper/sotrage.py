import json

from polite_scraper.config import OUTPUT_DIR


def write_books(records: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "books.json").write_text(json.dumps(records, indent=2, ensure_ascii=False))


def write_errors(errors: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "errors.json").write_text(json.dumps(errors, indent=2, ensure_ascii=False))