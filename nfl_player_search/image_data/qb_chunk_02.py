"""Assembled from _parts/qb_chunk_02; CHUNK matches monolith file."""
from pathlib import Path
_d = Path(__file__).resolve().parent / "_parts" / "qb_chunk_02"
CHUNK = "".join(p.read_text() for p in sorted(_d.glob("*.txt")))
