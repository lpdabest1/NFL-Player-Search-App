"""Assembled from _parts/wr_chunk_01/*.txt"""
from pathlib import Path

_PARTS = Path(__file__).resolve().parent / "_parts" / "wr_chunk_01"
DATA = "".join(p.read_text() for p in sorted(_PARTS.glob("*.txt")))
