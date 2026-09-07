"""Assemble compressed wr image payload."""
from . import wr_chunk_00, wr_chunk_01, wr_chunk_02, wr_chunk_03
DATA_B64 = "".join([
    wr_chunk_00.CHUNK,
    wr_chunk_01.CHUNK,
    wr_chunk_02.CHUNK,
    wr_chunk_03.CHUNK,
])
