"""Compressed 2021+ season CSV payloads (issue #6)."""
from __future__ import annotations

import base64
import io
import zlib
from importlib import import_module

import pandas as pd

_POS = {"QB": "qb", "RB": "rb", "WR": "wr"}


def load_modern_seasons(position_key: str) -> pd.DataFrame:
    """Load embedded 2021+ rows for QB/RB/WR."""
    mod = import_module(f"nfl_player_search.season_data.{_POS[position_key]}")
    raw = zlib.decompress(base64.b64decode(mod.DATA_B64))
    return pd.read_csv(io.BytesIO(raw))
