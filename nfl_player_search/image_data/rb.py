"""Assemble compressed RB image CSV payload."""
from . import rb_chunk_00, rb_chunk_01, rb_chunk_02, rb_chunk_03, rb_chunk_04, rb_chunk_05, rb_chunk_06, rb_chunk_07, rb_chunk_08, rb_chunk_09, rb_chunk_10, rb_chunk_11, rb_chunk_12, rb_chunk_13, rb_chunk_14, rb_chunk_15, rb_chunk_16
DATA_B64 = "".join([
    rb_chunk_00.CHUNK,
    rb_chunk_01.CHUNK,
    rb_chunk_02.CHUNK,
    rb_chunk_03.CHUNK,
    rb_chunk_04.CHUNK,
    rb_chunk_05.CHUNK,
    rb_chunk_06.CHUNK,
    rb_chunk_07.CHUNK,
    rb_chunk_08.CHUNK,
    rb_chunk_09.CHUNK,
    rb_chunk_10.CHUNK,
    rb_chunk_11.CHUNK,
    rb_chunk_12.CHUNK,
    rb_chunk_13.CHUNK,
    rb_chunk_14.CHUNK,
    rb_chunk_15.CHUNK,
    rb_chunk_16.CHUNK,
])
