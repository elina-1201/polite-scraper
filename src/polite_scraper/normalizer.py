# normalizer.py
import re
from datetime import datetime
from enum import IntEnum
from pydantic import BaseModel, model_validator

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


class Rating(IntEnum):
    One = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5


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
            match = re.search(r"[\d.]+", data.get("price_text", ""))
            if match:
                data["price_gbp"] = float(match.group())
            data["rating"] = RATING_MAP.get(data.get("rating_text"), 0)
        return data


def normalize_record(record: dict) -> dict:
    return BookRecord.model_validate(record).model_dump(mode="json")