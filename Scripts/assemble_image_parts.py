#!/usr/bin/env python3
"""Assemble image_data/_parts/<stem>/*.txt into image_data/<stem>.py monoliths."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1] / "nfl_player_search" / "image_data"
PARTS = ROOT / "_parts"
for d in sorted(PARTS.iterdir()):
    if not d.is_dir():
        continue
    texts = [p.read_text() for p in sorted(d.glob("*.txt"))]
    if not texts:
        continue
    out = ROOT / f"{d.name}.py"
    out.write_text("".join(texts))
    print(f"wrote {out.name} ({out.stat().st_size} bytes)")
