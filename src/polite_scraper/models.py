# models.py
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from pydantic import BaseModel, model_validator


class Rating(IntEnum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5


# Single source of truth for the (name -> value) mapping, derived from Rating.
RATING_MAP = {member.name: member.value for member in Rating}


class BookRecord(BaseModel):
    title: str
    product_url: str
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    rating: Rating
    description: str | None = None
    source_page: str
    fetched_at: datetime

    @model_validator(mode="before")
    @classmethod
    def derive_typed_fields(cls, data):
        """Convert raw text fields into typed values before validation."""
        if isinstance(data, dict):
            data = dict(data)
            data["rating"] = RATING_MAP.get(data.get("rating_text"), 0)
        return data


@dataclass
class RunSummary:
    start_time: str
    duration: float
    pages_fetched: int
    cache_hits: int
    valid_records: int
    invalid_records: int
    failed_pages: int

@dataclass
class RunResult:
    books: list[dict] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)
    logs: list[dict] = field(default_factory=list)
    summary: RunSummary | None = None