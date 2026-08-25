from pathlib import Path

# Project root: this file is src/polite_scraper/config.py
# go up 3 levels -> polite-scraper/
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Data directories (both gitignored)
CACHE_DIR = PROJECT_ROOT / "cache"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Network 
BASE_URL = "https://books.toscrape.com/"
USER_AGENT = "FlyRankInternship-A9/1.0 (https://github.com/elina-1201/polite-scraper)"
TIMEOUT = 10
PAGE_COUNT = 3          # first three catalogue pages (60 books)
DELAY_SECONDS = 1.0     # politeness delay between requests
