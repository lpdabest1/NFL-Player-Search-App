"""Assemble compressed qb image payload."""
from . import qb_chunk_00, qb_chunk_01
DATA_B64 = "".join([
    qb_chunk_00.CHUNK,
    qb_chunk_01.CHUNK,
])
