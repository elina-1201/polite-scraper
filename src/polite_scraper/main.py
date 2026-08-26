from polite_scraper.pipeline import run_pipeline

def main() -> None:
    result = run_pipeline()
    print(f"books={len(result.books)} errors={len(result.errors)}")