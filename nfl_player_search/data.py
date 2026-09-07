"""CSV loading helpers."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

from nfl_player_search.config import CategoryConfig


def _position_from_stats_path(stats_csv: str) -> str | None:
    name = Path(stats_csv).name.upper()
    if "NFL_QB" in stats_csv.replace("\\", "/") or name.startswith("NFL_QB"):
        return "QB"
    if "NFL_RB" in stats_csv.replace("\\", "/") or name.startswith("NFL_RB"):
        return "RB"
    if "NFL_WR" in stats_csv.replace("\\", "/") or name.startswith("NFL_WR"):
        return "WR"
    return None


@lru_cache(maxsize=8)
def load_stats(stats_csv: str, rename_items: tuple[tuple[str, str], ...] | None) -> pd.DataFrame:
    """Load and normalize a stats CSV. Paths are strings for cacheability.

    Seasons 2021+ are embedded via ``nfl_player_search.season_data`` (offline
    nflreadpy ETL output) and concatenated after dropping Year>=2021 from the
    base historical CSV.
    """
    path = Path(stats_csv)
    df = pd.read_csv(path)
    pos = _position_from_stats_path(stats_csv)
    if pos is not None:
        try:
            from nfl_player_search.season_data import load_modern_seasons
            modern = load_modern_seasons(pos)
            if "Year" in df.columns:
                df = df[pd.to_numeric(df["Year"], errors="coerce") < 2021]
            df = pd.concat([df, modern], ignore_index=True)
        except Exception:
            # Fall back to historical-only if embedded payload missing
            pass
    if rename_items:
        df = df.rename(columns=dict(rename_items))
    if "Year" in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")
    return df


def _position_from_images_path(images_csv: str) -> str | None:
    path = images_csv.replace("\\", "/")
    name = Path(images_csv).name.upper()
    if "NFL_QB" in path or name.startswith("NFL_QB"):
        return "QB"
    if "NFL_RB" in path or name.startswith("NFL_RB"):
        return "RB"
    if "NFL_WR" in path or name.startswith("NFL_WR"):
        return "WR"
    return None


@lru_cache(maxsize=8)
def load_images(images_csv: str) -> pd.DataFrame:
    """Load player image URL table (CSV preferred; embedded payload as fallback)."""
    path = Path(images_csv)
    if path.is_file():
        return pd.read_csv(path)
    pos = _position_from_images_path(images_csv)
    if pos is not None:
        from nfl_player_search.image_data import load_image_frame
        return load_image_frame(pos)
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
