"""CLI entry: append 2021-present seasons into committed CSVs."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from .builders import build_qb, build_rb, build_wr
from .constants import (
    APPEND_FROM_YEAR, QB_CSV, QB_HEADERS, RB_CSV, RB_HEADERS, WR_CSV, WR_HEADERS,
)
from .lookups import (
    build_team_map, latest_completed_season, load_age_lookup,
    load_gs_lookup, load_long_lookups, load_seasonal_stats,
)

def idempotent_write(path: Path, new_df: pd.DataFrame, headers: list[str]):
    hist = pd.read_csv(path)
    assert list(hist.columns) == headers, f"Header mismatch for {path}: {list(hist.columns)}"
    kept = hist[hist["Year"] < APPEND_FROM_YEAR].copy()
    combined = pd.concat([kept, new_df], ignore_index=True)
    combined.to_csv(path, index=False)
    return len(kept), len(new_df)

def run(start: int, end: int) -> None:
    seasons = list(range(start, end + 1))
    print(f"ETL seasons: {seasons}")
    print("Loading team map...")
    team_map = build_team_map()
    print("Loading seasonal player stats...")
    stats = load_seasonal_stats(seasons)
    print(f"  stats rows: {len(stats)}")
    print("Loading ages from players...")
    ages = load_age_lookup(seasons)
    print(f"  age rows: {len(ages)}")
    print("Loading Games Started from depth charts...")
    gs = load_gs_lookup(seasons)
    print(f"  GS rows: {len(gs)}")
    print("Loading longest plays from PBP...")
    pass_lng, rush_lng, rec_lng = load_long_lookups(seasons)
    print(f"  pass Lng: {len(pass_lng)}, rush Long: {len(rush_lng)}, rec Long: {len(rec_lng)}")
    print("Building QB/RB/WR frames...")
    qb = build_qb(stats, team_map, ages, gs, pass_lng)
    rb = build_rb(stats, team_map, ages, gs, rush_lng)
    wr = build_wr(stats, team_map, ages, gs, rec_lng)
    print(f"  QB {len(qb)}, RB {len(rb)}, WR {len(wr)}")
    print("Writing CSVs (idempotent: drop Year>=2021 then append)...")
    k, n = idempotent_write(QB_CSV, qb, QB_HEADERS)
    print(f"  QB: kept {k} historical, appended {n}")
    k, n = idempotent_write(RB_CSV, rb, RB_HEADERS)
    print(f"  RB: kept {k} historical, appended {n}")
    k, n = idempotent_write(WR_CSV, wr, WR_HEADERS)
    print(f"  WR: kept {k} historical, appended {n}")
    for label, df in (("QB", qb), ("RB", rb), ("WR", wr)):
        age_miss = df["Age"].isna().mean() * 100
        gs_miss = df["Games Started"].isna().mean() * 100
        long_col = "Longest Pass" if label == "QB" else "Long"
        lng_miss = df[long_col].isna().mean() * 100
        print(f"  gaps {label}: Age NaN {age_miss:.1f}%, GS NaN {gs_miss:.1f}%, {long_col} NaN {lng_miss:.1f}%")
    print("Done.")

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=int, default=APPEND_FROM_YEAR)
    parser.add_argument("--end", type=int, default=None, help="Last season inclusive")
    args = parser.parse_args()
    end = args.end if args.end is not None else latest_completed_season()
    if end < args.start:
        raise SystemExit(f"No seasons to append (start={args.start}, end={end})")
    run(args.start, end)

if __name__ == "__main__":
    main()
