"""Assemble compressed qb payload."""
from . import qb_chunk_00, qb_chunk_01, qb_chunk_02, qb_chunk_03, qb_chunk_04, qb_chunk_05, qb_chunk_06, qb_chunk_07, qb_chunk_08, qb_chunk_09, qb_chunk_10, qb_chunk_11
DATA_B64 = "".join([
    qb_chunk_00.CHUNK,
    qb_chunk_01.CHUNK,
    qb_chunk_02.CHUNK,
    qb_chunk_03.CHUNK,
    qb_chunk_04.CHUNK,
    qb_chunk_05.CHUNK,
    qb_chunk_06.CHUNK,
    qb_chunk_07.CHUNK,
    qb_chunk_08.CHUNK,
    qb_chunk_09.CHUNK,
    qb_chunk_10.CHUNK,
    qb_chunk_11.CHUNK,
])
