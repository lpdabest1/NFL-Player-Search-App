"""Assembled from _parts/rb_chunk_03/*.txt"""
from pathlib import Path

_PARTS = Path(__file__).resolve().parent / "_parts" / "rb_chunk_03"
DATA = "".join(p.read_text() for p in sorted(_PARTS.glob("*.txt")))
