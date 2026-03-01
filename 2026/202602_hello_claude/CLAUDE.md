# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
cd news-collector
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-api-key"
```

## Running

```bash
cd news-collector
python main.py
```

## Architecture

The `news-collector/` pipeline runs in four sequential steps orchestrated by `main.py`:

1. **`fetcher.py`** — Parses RSS feeds via `feedparser`, deduplicates against `data/posted.json`, and returns new articles (up to `MAX_ARTICLES_PER_SOURCE` per source).
2. **`summarizer.py`** — Calls `claude-haiku-4-5-20251001` via the Anthropic SDK to produce a Japanese summary (≤150 chars) for each article. Falls back to the article title on error.
3. **`reporter.py`** — Renders a self-contained HTML file to `output/YYYYMMDD_HHMM_news.html` with a TOP3 section and tabbed source views.
4. **`main.py`** — Runs the pipeline and opens the HTML in the browser with `open`.

**Config** (`config.py`): All tunable constants live here — RSS source URLs, `MAX_ARTICLES_PER_SOURCE`, `SUMMARY_MAX_CHARS`, `CLAUDE_MODEL`, output paths.

**State**: `data/posted.json` tracks fetched URLs to avoid re-processing on subsequent runs.

## Notes

- All output is Japanese, including AI summaries of English-language articles.
- The `news-collector/` files were deleted from the working tree in the second commit but exist in git history at `3668da5`. The restored `main.py` is the only file currently on disk.
