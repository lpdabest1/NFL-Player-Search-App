"""Assembled from _parts/rb_chunk_03; exec restores CHUNK like monolith."""
from pathlib import Path
_src = "".join(p.read_text() for p in sorted((Path(__file__).resolve().parent / "_parts" / "rb_chunk_03").glob("*.txt")))
exec(_src, globals())
