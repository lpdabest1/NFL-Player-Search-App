"""Assembled from _parts/qb_chunk_04; exec restores CHUNK like monolith."""
from pathlib import Path
_src = "".join(p.read_text() for p in sorted((Path(__file__).resolve().parent / "_parts" / "qb_chunk_04").glob("*.txt")))
exec(_src, globals())
