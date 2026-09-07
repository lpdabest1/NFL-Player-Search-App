"""Assemble compressed rb image payload."""
from . import rb_chunk_00, rb_chunk_01, rb_chunk_02, rb_chunk_03
DATA_B64 = "".join([
    rb_chunk_00.CHUNK,
    rb_chunk_01.CHUNK,
    rb_chunk_02.CHUNK,
    rb_chunk_03.CHUNK,
])
