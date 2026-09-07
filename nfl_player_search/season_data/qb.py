"""Assemble compressed qb payload."""
from . import qb_chunk_00, qb_chunk_01, qb_chunk_02, qb_chunk_03
DATA_B64 = "".join([
    qb_chunk_00.CHUNK,
    qb_chunk_01.CHUNK,
    qb_chunk_02.CHUNK,
    qb_chunk_03.CHUNK,
])
