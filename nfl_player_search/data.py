"""CSV loading helpers."""

from __future__ import annotations

from functools import lru_cache

import pandas as pd

from nfl_player_search.config import CategoryConfig


@lru_cache(maxsize=8)
def load_stats(stats_csv: str, rename_items: tuple[tuple[str, str], ...] | None) -> pd.DataFrame:
    """Load and normalize a stats CSV. Paths are strings for cacheability."""
    df = pd.read_csv(stats_csv)
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
