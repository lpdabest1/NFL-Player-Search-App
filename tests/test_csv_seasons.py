"""Smoke: embedded modern seasons load with historical CSVs."""

from __future__ import annotations

import pytest
import pandas as pd

from nfl_player_search.config import PASSING, RECEIVING, RUSHING
from nfl_player_search.data import load_stats


def _payloads_present() -> bool:
    try:
        from nfl_player_search.season_data import load_modern_seasons
        df = load_modern_seasons("QB")
        return int(df["Year"].min()) >= 2021
    except Exception:
        return False


@pytest.mark.skipif(not _payloads_present(), reason="season_data chunk payloads not committed yet")
def test_stats_csvs_include_2021_plus_and_keep_headers() -> None:
    configs = [
        (
            PASSING,
            [
                "Player", "Team", "Age", "Games Played", "Games Started",
                "Passes Completed", "Passes Attempted", "Completion Percentage",
                "Passing Yards", "Passing Touchdowns", "Touchdown Percentage",
                "Interceptions", "Interceptions Percentage", "Longest Pass",
                "Yards Per Attempt", "Adjusted Yards Per Attempt",
                "Yards per Completion", "Yards Per Game", "Passer Rating", "Year",
            ],
            ["Cmp%", "Yds", "TD", "TD%", "INT%", "Rating"],
        ),
        (
            RUSHING,
            [
                "Player", "Team", "Age", "Games Played", "Games Started",
                "Att", "Yards", "TD", "Long", "Y/A", "Y/G", "Fumbles", "Year",
            ],
            ["Att", "Yards", "TD", "Y/A", "Y/G"],
        ),
        (
            RECEIVING,
            [
                "Player", "Team", "Age", "Games Played", "Games Started",
                "Rec", "Yards", "Y/C", "TD", "Long", "Rec/G", "Y/G", "Year",
            ],
            ["Rec", "Yards", "TD", "Y/C", "Rec/G", "Y/G"],
        ),
    ]

    for cfg, headers, radar_src in configs:
        raw = pd.read_csv(cfg.stats_csv)
        assert list(raw.columns) == headers
        assert raw["Year"].max() == 2020

        rename_items = tuple(cfg.rename_map.items()) if cfg.rename_map else None
        df = load_stats(str(cfg.stats_csv), rename_items)
        years = set(df["Year"].dropna().astype(int))
        assert 1960 in years and 2020 in years and 2021 in years
        assert max(years) >= 2024
        for col in radar_src:
            assert col in df.columns, f"{cfg.key}: missing radar col {col}"
            assert df.loc[df["Year"] >= 2021, col].notna().any()
