#!/usr/bin/env python3
"""Offline ETL: rebuild QB/RB/WR *_Search_Images.csv from nflreadpy headshots.

Dev-only dependency: nflreadpy (see requirements-dev.txt). No Streamlit Cloud fetch.

Usage (from repo root):
    python Scripts/etl_nflreadpy_headshots.py
    python Scripts/etl_nflreadpy_headshots.py --stats-start 1999 --stats-end 2025
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nflreadpy_etl.headshots_cli import main

if __name__ == "__main__":
    main()
