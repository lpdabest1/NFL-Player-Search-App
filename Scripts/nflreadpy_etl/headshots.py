"""Rebuild committed player headshot URL CSVs from nflreadpy (dev-only).

Join strategy (prefer stable IDs):
1. Build gsis_id -> URL from load_players().headshot, overridden by the latest
   non-null headshot_url from load_player_stats (1999-present) when present.
2. Resolve each stats-CSV Player display name -> gsis_id via
   load_players().display_name (and stats player_display_name as fallback),
   preferring position-matched rows on name collisions.
3. Emit one row per unique Player in the position's stats (historical CSV +
   embedded season_data): Player, Player Image (URL or empty).

No PFR scrape. Idempotent full rewrite of the three *_Search_Images.csv files.
"""
from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd

from .constants import (
    IMAGE_HEADERS,
    POSITION_PREFERENCE,
    QB_CSV,
    QB_IMAGES_CSV,
    RB_CSV,
    RB_IMAGES_CSV,
    REPO_ROOT,
    WR_CSV,
    WR_IMAGES_CSV,
)


def _load_unique_players(stats_csv: Path, position_key: str) -> list[str]:
    """Unique Player names matching what the UI loads (hist CSV + modern embeds)."""
    hist = pd.read_csv(stats_csv)
    if "Year" in hist.columns:
        hist = hist[pd.to_numeric(hist["Year"], errors="coerce") < 2021]
    frames = [hist]
    try:
        import sys

        sys.path.insert(0, str(REPO_ROOT))
        from nfl_player_search.season_data import load_modern_seasons

        frames.append(load_modern_seasons(position_key))
    except Exception as exc:  # noqa: BLE001
        print(f"  warning: modern season_data for {position_key}: {exc}")
    combined = pd.concat(frames, ignore_index=True)
    names = (
        combined["Player"]
        .dropna()
        .astype(str)
        .str.strip()
        .loc[lambda s: s.ne("")]
        .unique()
        .tolist()
    )
    return sorted(names)


def _build_gsis_url_map(stats_seasons: Iterable[int]) -> pd.DataFrame:
    """Return DataFrame indexed by gsis_id with columns url, display_name, position, last_season."""
    import nflreadpy as nfl

    players = nfl.load_players().to_pandas()
    players = players.dropna(subset=["gsis_id"]).drop_duplicates("gsis_id", keep="last")
    base = players[
        ["gsis_id", "display_name", "position", "last_season", "headshot"]
    ].copy()
    base = base.rename(columns={"headshot": "players_url"})

    seasons = list(stats_seasons)
    print(f"  loading player_stats seasons {seasons[0]}-{seasons[-1]} for URLs...")
    stats = nfl.load_player_stats(seasons, summary_level="reg").to_pandas()
    latest = (
        stats.dropna(subset=["player_id"])
        .sort_values("season")
        .groupby("player_id", as_index=False)
        .agg(
            stats_url=("headshot_url", "last"),
            stats_display=("player_display_name", "last"),
            stats_position=("position", "last"),
            stats_last_season=("season", "last"),
        )
    )
    merged = base.merge(latest, left_on="gsis_id", right_on="player_id", how="left")
    merged["url"] = merged["stats_url"].fillna(merged["players_url"])
    merged["display_name"] = merged["stats_display"].fillna(merged["display_name"])
    merged["position"] = merged["stats_position"].fillna(merged["position"])
    merged["last_season"] = merged["stats_last_season"].fillna(merged["last_season"])
    out = merged[["gsis_id", "display_name", "position", "last_season", "url"]].copy()
    print(
        f"  gsis map: {len(out)} ids, URL coverage {out['url'].notna().mean()*100:.1f}%"
    )
    return out


def _name_to_gsis(gsis_map: pd.DataFrame, position_key: str) -> pd.DataFrame:
    """Map display_name -> best gsis row for this position CSV."""
    preferred = POSITION_PREFERENCE.get(position_key, ())
    df = gsis_map.dropna(subset=["display_name"]).copy()
    df["display_name"] = df["display_name"].astype(str).str.strip()
    df["pos_match"] = df["position"].isin(preferred) if preferred else False
    df["has_url"] = df["url"].notna() & df["url"].astype(str).str.strip().ne("")
    df = df.sort_values(
        ["pos_match", "has_url", "last_season"],
        ascending=[False, False, False],
    )
    return df.drop_duplicates("display_name", keep="first").set_index("display_name")


def build_image_frame(player_names: list[str], name_index: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name in player_names:
        url = ""
        if name in name_index.index:
            raw = name_index.loc[name, "url"]
            if pd.notna(raw) and str(raw).strip():
                url = str(raw).strip()
        rows.append({"Player": name, "Player Image": url})
    out = pd.DataFrame(rows, columns=IMAGE_HEADERS)
    return out


def write_images_csv(path: Path, frame: pd.DataFrame) -> tuple[int, int]:
    assert list(frame.columns) == IMAGE_HEADERS
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)
    with_url = int((frame["Player Image"].astype(str).str.strip() != "").sum())
    return len(frame), with_url


def run_headshots(stats_start: int = 1999, stats_end: int | None = None) -> dict:
    from .lookups import latest_completed_season

    end = stats_end if stats_end is not None else latest_completed_season()
    seasons = list(range(stats_start, end + 1))
    gsis_map = _build_gsis_url_map(seasons)

    jobs = [
        ("QB", QB_CSV, QB_IMAGES_CSV),
        ("RB", RB_CSV, RB_IMAGES_CSV),
        ("WR", WR_CSV, WR_IMAGES_CSV),
    ]
    summary: dict[str, dict] = {}
    for key, stats_csv, images_csv in jobs:
        print(f"Building {key} image CSV...")
        names = _load_unique_players(stats_csv, key)
        name_index = _name_to_gsis(gsis_map, key)
        frame = build_image_frame(names, name_index)
        n, with_url = write_images_csv(images_csv, frame)
        try:
            import sys

            sys.path.insert(0, str(REPO_ROOT))
            from nfl_player_search.season_data import load_modern_seasons

            modern_names = set(
                load_modern_seasons(key)["Player"].dropna().astype(str).str.strip()
            )
        except Exception:
            modern_names = set()
        modern_with = sum(
            1
            for n in modern_names
            if n in name_index.index
            and pd.notna(name_index.loc[n, "url"])
            and str(name_index.loc[n, "url"]).strip()
        )
        modern_rate = (modern_with / len(modern_names) * 100) if modern_names else 0.0
        overall_rate = with_url / n * 100 if n else 0.0
        print(
            f"  {key}: {with_url}/{n} URLs ({overall_rate:.1f}%); "
            f"modern {modern_with}/{len(modern_names)} ({modern_rate:.1f}%) -> {images_csv}"
        )
        summary[key] = {
            "players": n,
            "with_url": with_url,
            "overall_pct": overall_rate,
            "modern_players": len(modern_names),
            "modern_with_url": modern_with,
            "modern_pct": modern_rate,
            "path": str(images_csv),
        }
    return summary
