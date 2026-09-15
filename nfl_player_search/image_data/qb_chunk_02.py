"""Assembled from _parts/qb_chunk_02/*.txt"""
from pathlib import Path

_PARTS = Path(__file__).resolve().parent / "_parts" / "qb_chunk_02"
DATA = "".join(p.read_text() for p in sorted(_PARTS.glob("*.txt")))
