#!/usr/bin/env python3
"""Offline ETL: append nflreadpy seasons 2021-present into committed QB/RB/WR CSVs.

Dev-only dependency: nflreadpy (see requirements-dev.txt). Does not run on Streamlit Cloud.

Usage (from repo root):
    python Scripts/etl_nflreadpy_append.py
    python Scripts/etl_nflreadpy_append.py --start 2021 --end 2025
"""
from __future__ import annotations
import sys
from pathlib import Path

# Allow `python Scripts/etl_nflreadpy_append.py` without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nflreadpy_etl.cli import main

if __name__ == "__main__":
    main()
