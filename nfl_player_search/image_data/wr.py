"""Assemble compressed WR image CSV payload."""
from . import wr_chunk_00, wr_chunk_01, wr_chunk_02, wr_chunk_03, wr_chunk_04, wr_chunk_05, wr_chunk_06, wr_chunk_07, wr_chunk_08
DATA_B64 = "".join([
    wr_chunk_00.CHUNK,
    wr_chunk_01.CHUNK,
    wr_chunk_02.CHUNK,
    wr_chunk_03.CHUNK,
    wr_chunk_04.CHUNK,
    wr_chunk_05.CHUNK,
    wr_chunk_06.CHUNK,
    wr_chunk_07.CHUNK,
    wr_chunk_08.CHUNK,
])
