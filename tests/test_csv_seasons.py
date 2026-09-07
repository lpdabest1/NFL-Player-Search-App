"""Smoke: committed CSVs include appended modern seasons."""

from __future__ import annotations

import pandas as pd

from nfl_player_search.config import PASSING, RECEIVING, RUSHING


def test_stats_csvs_include_2021_plus_and_keep_headers() -> None:
    configs = [
        (
            PASSING,
            [
                "Player",
                "Team",
                "Age",
                "Games Played",
                "Games Started",
                "Passes Completed",
                "Passes Attempted",
                "Completion Percentage",
                "Passing Yards",
                "Passing Touchdowns",
                "Touchdown Percentage",
                "Interceptions",
                "Interceptions Percentage",
                "Longest Pass",
                "Yards Per Attempt",
                "Adjusted Yards Per Attempt",
                "Yards per Completion",
                "Yards Per Game",
                "Passer Rating",
                "Year",
            ],
            ["Cmp%", "Yds", "TD", "TD%", "INT%", "Rating"],
        ),
        (
            RUSHING,
            [
                "Player",
                "Team",
                "Age",
                "Games Played",
                "Games Started",
                "Att",
                "Yards",
                "TD",
                "Long",
                "Y/A",
                "Y/G",
                "Fumbles",
                "Year",
            ],
            ["Att", "Yards", "TD", "Y/A", "Y/G"],
        ),
        (
            RECEIVING,
            [
                "Player",
                "Team",
                "Age",
                "Games Played",
                "Games Started",
                "Rec",
                "Yards",
                "Y/C",
                "TD",
                "Long",
                "Rec/G",
                "Y/G",
                "Year",
            ],
            ["Rec", "Yards", "TD", "Y/C", "Rec/G", "Y/G"],
        ),
    ]

    for cfg, headers, radar_src in configs:
        df = pd.read_csv(cfg.stats_csv)
        assert list(df.columns) == headers
        years = set(df["Year"].dropna().astype(int))
        assert 1960 in years
        assert 2020 in years
        assert 2021 in years
        assert max(years) >= 2024
        recent = df[df["Year"] >= 2021]
        assert len(recent) > 0
        # Radar inputs must be present after rename (or as native headers).
        work = df.rename(columns=dict(cfg.rename_map or {}))
        for col in radar_src:
            assert col in work.columns, f"{cfg.key}: missing radar col {col}"
            assert work.loc[work["Year"] >= 2021, col].notna().any()
