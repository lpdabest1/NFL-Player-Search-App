from . import qb_chunk_00, qb_chunk_01, qb_chunk_02, qb_chunk_03

DATA_B64 = "".join([
    qb_chunk_00.DATA,
    qb_chunk_01.DATA,
    qb_chunk_02.DATA,
    qb_chunk_03.DATA,
])
