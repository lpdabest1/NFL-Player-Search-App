#!/usr/bin/env python3
"""Offline ETL: refresh QB/RB/WR Player Image CSVs from nflverse headshots (issue #4).

Dev-only dependency: nflreadpy (see requirements-dev.txt). Does not run on Streamlit Cloud.
Commits plain CSVs (same offline pattern as #6; no live Cloud scrape).

Usage (from repo root):
    python Scripts/etl_headshots_refresh.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT))

from nflreadpy_etl.headshots import refresh_all  # noqa: E402


def main() -> None:
    summary = refresh_all()
    print("Done.")
    for pos, info in summary.items():
        print(f"  {pos}: {info['players_with_url']}/{info['players_total']} ({info['coverage_pct']}%)")


if __name__ == "__main__":
    main()
