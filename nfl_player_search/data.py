"""CSV loading helpers."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

from nfl_player_search.config import CategoryConfig


def _modern_season_shards(stats_path: Path) -> list[Path]:
    """Return nflreadpy season shard CSVs: ``NFL_QB_Search_2021.csv`` etc."""
    return sorted(stats_path.parent.glob(f"{stats_path.stem}_20[2-9][0-9].csv"))


@lru_cache(maxsize=8)
def load_stats(stats_csv: str, rename_items: tuple[tuple[str, str], ...] | None) -> pd.DataFrame:
    """Load and normalize a stats CSV. Paths are strings for cacheability.

    Modern seasons (2021+) may live in sibling shard files named
    ``{stem}_YYYY.csv`` produced by the nflreadpy ETL. Those are concatenated
    after dropping Year>=2021 from the base file (idempotent with a fully
    refreshed base CSV).
    """
    path = Path(stats_csv)
    df = pd.read_csv(path)
    shards = _modern_season_shards(path)
    if shards:
        if "Year" in df.columns:
            df = df[pd.to_numeric(df["Year"], errors="coerce") < 2021]
        parts = [df] + [pd.read_csv(p) for p in shards]
        df = pd.concat(parts, ignore_index=True)
    if rename_items:
        df = df.rename(columns=dict(rename_items))
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    return df


@lru_cache(maxsize=8)
def load_images(images_csv: str) -> pd.DataFrame:
    """Load player image URL CSV."""
    return pd.read_csv(images_csv)


def load_category_frames(config: CategoryConfig) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (stats, images) for a category."""
    rename_items = tuple(config.rename_map.items()) if config.rename_map else None
    stats = load_stats(str(config.stats_csv), rename_items).copy()
    images = load_images(str(config.images_csv)).copy()
    return stats, images


def player_years(stats: pd.DataFrame, player: str) -> list[int]:
    years = stats.loc[stats["Player"] == player, "Year"].dropna().astype(int).tolist()
    return years


def player_team_for_year(stats: pd.DataFrame, player: str, year: int) -> str:
    rows = stats.loc[(stats["Player"] == player) & (stats["Year"] == year), "Team"]
    if rows.empty:
        return ""
    return str(rows.iloc[0])
