"""Assemble compressed WR image CSV payload."""
from . import wr_chunk_00, wr_chunk_01, wr_chunk_02, wr_chunk_03, wr_chunk_04, wr_chunk_05, wr_chunk_06, wr_chunk_07, wr_chunk_08, wr_chunk_09, wr_chunk_10, wr_chunk_11, wr_chunk_12, wr_chunk_13, wr_chunk_14, wr_chunk_15, wr_chunk_16, wr_chunk_17, wr_chunk_18, wr_chunk_19, wr_chunk_20
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
    wr_chunk_09.CHUNK,
    wr_chunk_10.CHUNK,
    wr_chunk_11.CHUNK,
    wr_chunk_12.CHUNK,
    wr_chunk_13.CHUNK,
    wr_chunk_14.CHUNK,
    wr_chunk_15.CHUNK,
    wr_chunk_16.CHUNK,
    wr_chunk_17.CHUNK,
    wr_chunk_18.CHUNK,
    wr_chunk_19.CHUNK,
    wr_chunk_20.CHUNK
])
