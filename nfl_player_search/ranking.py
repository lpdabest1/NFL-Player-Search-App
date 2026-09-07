"""Percentile ranks and composite player ratings."""

from __future__ import annotations

from typing import Mapping, Sequence

import pandas as pd


def add_percentile_ranks(
    df: pd.DataFrame,
    stats: Sequence[str],
    invert: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Add `<stat> Rank` percentile columns (0–1). Higher is better unless inverted."""
    out = df.copy()
    invert_set = set(invert or [])
    for stat in stats:
        out[stat] = pd.to_numeric(out[stat], errors="coerce")
        rank = out[stat].rank(pct=True)
        if stat in invert_set:
            rank = 1 - rank
        out[f"{stat} Rank"] = rank
    return out


def compute_player_ratings(
    ranked: pd.DataFrame,
    weights: Mapping[str, float],
) -> pd.DataFrame:
    """Weighted sum of percentile ranks → `Player Rating`, sorted descending."""
    score = pd.Series(0.0, index=ranked.index)
    for stat, weight in weights.items():
        col = f"{stat} Rank"
        if col not in ranked.columns:
            raise KeyError(f"Missing rank column: {col}")
        score = score + ranked[col].astype(float) * float(weight)
    out = ranked[["Player"]].copy()
    out["Player Rating"] = score
    return out.sort_values("Player Rating", ascending=False).reset_index(drop=True)


def season_leaderboard_size(year: int) -> int:
    """Historical pool size used by the original app (pre-1970 vs modern)."""
    if 1960 <= year < 1970:
        return 20
    return 32


def player_rank_among(ratings: pd.DataFrame, player: str) -> tuple[int, int]:
    """Return (1-based rank, pool size). Rank is -1 if player not in pool."""
    players = ratings["Player"].tolist()
    pool = len(players)
    if player not in players:
        return -1, pool
    return players.index(player) + 1, pool
