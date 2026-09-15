"""Assembled from _parts/wr_chunk_13/*.txt"""
from pathlib import Path

_PARTS = Path(__file__).resolve().parent / "_parts" / "wr_chunk_13"
DATA = "".join(p.read_text() for p in sorted(_PARTS.glob("*.txt")))
