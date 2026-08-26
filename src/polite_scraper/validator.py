from pydantic import ValidationError

from polite_scraper.models import BookRecord


def error_entry(raw: dict, exc: ValidationError) -> dict:
    """Build a structured error dict from a raw record + its ValidationError."""
    return {
        "product_url": raw.get("product_url"),
        "source_page": raw.get("source_page"),
        "raw_record": raw,
        "errors": exc.errors(),
    }


def validate_record(raw: dict) -> tuple[dict | None, dict | None]:
    """Validate a raw record."""
    try:
        return BookRecord.model_validate(raw).model_dump(mode="json"), None
    except ValidationError as exc:
        return None, error_entry(raw, exc)