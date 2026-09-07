"""Compressed Player Image CSV payloads (issue #4)."""
from __future__ import annotations

import base64
import io
import zlib
from importlib import import_module

import pandas as pd

_POS = {"QB": "qb", "RB": "rb", "WR": "wr"}


def load_image_frame(position_key: str) -> pd.DataFrame:
    """Load embedded Player/Player Image table for QB/RB/WR."""
    mod = import_module(f"nfl_player_search.image_data.{_POS[position_key]}")
    raw = zlib.decompress(base64.b64decode(mod.DATA_B64))
    return pd.read_csv(io.BytesIO(raw))
