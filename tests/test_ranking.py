"""Unit tests for ranking helpers (no Streamlit required)."""

from __future__ import annotations

import pandas as pd

from nfl_player_search.ranking import (
    add_percentile_ranks,
    compute_player_ratings,
    player_rank_among,
    season_leaderboard_size,
)


def test_add_percentile_ranks_and_invert() -> None:
    df = pd.DataFrame(
        {
            "Player": ["A", "B", "C"],
            "Yds": [3000, 2000, 1000],
            "INT%": [1.0, 2.0, 3.0],
        }
    )
    ranked = add_percentile_ranks(df, ["Yds", "INT%"], invert=["INT%"])
    assert ranked.loc[ranked["Player"] == "A", "Yds Rank"].iloc[0] == ranked["Yds Rank"].max()
    assert ranked.loc[ranked["Player"] == "C", "Yds Rank"].iloc[0] == ranked["Yds Rank"].min()
    # Lower INT% should rank better after invert
    assert ranked.loc[ranked["Player"] == "A", "INT% Rank"].iloc[0] == ranked["INT% Rank"].max()


def test_compute_player_ratings_order() -> None:
    ranked = pd.DataFrame(
        {
            "Player": ["A", "B"],
            "Yds Rank": [1.0, 0.5],
            "TD Rank": [0.5, 1.0],
        }
    )
    ratings = compute_player_ratings(ranked, {"Yds": 10.0, "TD": 10.0})
    assert list(ratings["Player"]) == ["A", "B"]
    assert ratings.iloc[0]["Player Rating"] == 15.0


def test_season_leaderboard_size() -> None:
    assert season_leaderboard_size(1965) == 20
    assert season_leaderboard_size(1999) == 32


def test_player_rank_among() -> None:
    ratings = pd.DataFrame({"Player": ["A", "B", "C"], "Player Rating": [3, 2, 1]})
    assert player_rank_among(ratings, "B") == (2, 3)
    assert player_rank_among(ratings, "Z") == (-1, 3)
