# Polite scraper

A small, polite scraping pipeline. It downloads the first three catalogue pages of Books to Scrape, visits all 60 book pages, turns messy HTML into clean, checked JSON records, survives a broken page without crashing, and ends every run with a short report of what happened.

> I will not reuse this code on another site without checking its rules and terms first
# Target classification

This scraper targets a single, well-defined site for learning purposes.

- **Target site:** [Books to Scrape](https://books.toscrape.com/catalogue/category/books_1/index.html)
- **Why:** To learn web scraping in a safe, real-world context.
- **Scope:** The first three catalogue pages only (60 `HTML` pages).
- **Data collected:** Book name, price, rating, and stock availability.
- **Why this is appropriate:** The website is explicitly designed to be scraped — as stated on its homepage — making it an ideal and legitimate target for practice.

# Notes

## Robots.txt
The website returns `404 - Not found` after requesting `https://books.toscrape.com/robots.txt`

