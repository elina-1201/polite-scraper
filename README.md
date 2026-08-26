# Polite scraper

A small, polite scraping pipeline. It downloads the first three catalogue pages of Books to Scrape, visits all 60 book detail pages, turns messy HTML into clean, checked JSON records, survives a broken page without crashing, and ends every run with a short report of what happened.

> I will not reuse this code on another site without checking its rules and terms first.

## Lane

This scraper runs in the **static HTML** lane: Books to Scrape serves the full catalogue and every book's data as plain, server-rendered HTML. That means the scraper only needs `requests` + `BeautifulSoup` — **no browser** — which keeps it lightweight and cheap.

## Setup

**Prerequisites**

- **[uv](https://docs.astral.sh/uv/)** — the package manager used to install dependencies and run the tool.

### Install

Clone the repository and sync dependencies into a local virtual environment:

```bash
git clone https://github.com/elina-1201/polite-scraper.git
cd polite-scraper
uv sync
```

### Run

Launch the scraper in one line:

```bash
uv run polite-scraper
```

## Target classification (Stage 0)

This scraper targets a single, well-defined site for learning purposes.

- **Target site:** [Books to Scrape](https://books.toscrape.com/)
- **Why:** To learn web scraping in a safe, real-world context.
- **Scope:** The first three catalogue pages only (60 book `HTML` pages).
- **Data collected:** Book title, price, rating, description and stock availability.
- **Why this is appropriate:** The website's homepage states it is explicitly designed to be scraped, making it a legitimate target for practice.

## Record schema

Each item in `output/books.json` is a validated `BookRecord` (see the [Pydantic](https://docs.pydantic.dev/) model in `models.py`). Here is the example of the record:

```json
{
  "title": "A Light in the Attic",
  "product_url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
  "price_text": "£51.77",
  "price_gbp": 51.77,
  "availability_text": "In stock (22 available)",
  "rating_text": "Three",
  "rating": 3,
  "description": "It's hard to imagine a world without A Light in the Attic... ...more",
  "source_page": "https://books.toscrape.com/",
  "fetched_at": "2026-08-26T19:01:27.017443"
}
```

| Field | Type | Notes |
| --- | --- | --- |
| `title` | string | Book title from the `<h1>`. |
| `product_url` | string | Canonical URL of the book detail page. |
| `price_text` | string | Raw price text, e.g. `£51.77`. |
| `price_gbp` | number | Price parsed to a `float`. |
| `availability_text` | string | Raw stock text, e.g. `In stock (22 available)`. |
| `rating_text` | string | Rating word, e.g. `Three`. |
| `rating` | integer | Rating mapped to an int from 1–5 (an `IntEnum`). |
| `description` | string or `null` | Description text, `null` when absent. |
| `source_page` | string | The catalogue page the book link was found on. |
| `fetched_at` | timestamp | When the record was created (ISO 8601). |

## Politeness rules

The scraper is deliberately gentle, and waits at least a second between real requests:

- **User-Agent:** `FlyRankInternship-A9/1.0 (https://github.com/elina-1201/polite-scraper)` — the scraper identifies itself and links back to this repo.
- **Delay:** `1.0s` between real HTTP requests (never under half a second), enforced in `fetcher._politeness_delay()`. Cached pages skip this entirely.
- **Timeout:** `10s` per request.
- **Retries:** 1 retry (`MAX_RETRIES = 1`) after a `2s` wait, but only for timeouts, connection errors, and 5xx responses — 4xx errors are never retried.
- **Cache:** Each page is cached locally (`cache/pages/` for catalogue pages, `cache/items/` for book details). A cache hit skips the network completely — no request, no delay, no cost — which is why a warmed run reports high `cache_hits` and few `pages_fetched`.

## Honest limitation

This lane uses plain HTTP only, so it **cannot render JavaScript**. That is fine for Books to Scrape, which is fully server-rendered — but the moment a target renders its catalogue client-side or behind a login, this scraper would silently return nothing rather than failing loudly.

## Proof: a real run report

This is the latest full run from `output/run-report.json`:

```json
{
  "start_time": "2026-08-26T19:01:26.298742",
  "duration": 60.70854634800344,
  "pages_fetched": 64,
  "cache_hits": 0,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1
}
```

It fetched all 60 book pages plus the three catalogue pages plus one hardcoded broken link (`pages_fetched = 64`), validated all 60 records, and reported a single `failed_pages` — the result of a deliberately injected broken link used to prove the pipeline survives an unreachable page without crashing (no records were lost).

This assignment needed **no browser** because all the data is already in the HTML the server sends, so a browser would only add cost and complexity.

## Ethics

Where possible, an official API should be used instead of scraping the web, both because it is more stable for the program and because unnecessary traffic is not generated. If a `403` error, a paywall, a login, or other blocks are encountered, they should not be bypassed; instead, the request should be abandoned. Only the information that is needed and that is public should be scraped. Before a scrape is started, the website's policy should be read and its `robots.txt` should be checked.

## Robots.txt
The website returns `404 - Not found` after requesting `https://books.toscrape.com/robots.txt`

