"""Shared configuration for categories, paths, and team colors."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Mapping

# Repo root = parent of this package when installed as a sibling of CSV_Files
REPO_ROOT = Path(__file__).resolve().parent.parent

TEAM_COLORS: Dict[str, str] = {
    "Arizona Cardinals": "#97233f",
    "Atlanta Falcons": "#a71930",
    "Baltimore Ravens": "#241773",
    "Buffalo Bills": "#00338d",
    "Carolina Panthers": "#0085ca",
    "Chicago Bears": "#0b162a",
    "Cincinnati Bengals": "#fb4f14",
    "Cleveland Browns": "#311d00",
    "Dallas Cowboys": "#041e42",
    "Denver Broncos": "#002244",
    "Detroit Lions": "#0076b6",
    "Green Bay Packers": "#203731",
    "Houston Texans": "#03202f",
    "Indianapolis Colts": "#002c5f",
    "Jacksonville Jaguars": "#006778",
    "Kansas City Chiefs": "#e31837",
    "Los Angeles Chargers": "#002a5e",
    "Los Angeles Rams": "#003594",
    "Miami Dolphins": "#008e97",
    "Minnesota Vikings": "#4f2683",
    "New England Patriots": "#002244",
    "New Orleans Saints": "#d3bc8d",
    "New York Giants": "#0b2265",
    "New York Jets": "#125740",
    "Las Vegas Raiders": "#000000",
    "Philadelphia Eagles": "#004c54",
    "Pittsburgh Steelers": "#ffb612",
    "San Francisco 49ers": "#aa0000",
    "Seattle Seahawks": "#002244",
    "Tampa Bay Buccaneers": "#d50a0a",
    "Tennessee Titans": "#0c2340",
    "Washington Football Team": "#773141",
    "Washington Commanders": "#773141",
}


@dataclass(frozen=True)
class CategoryConfig:
    """Per-position configuration for data loading and ranking."""

    key: str
    label: str
    noun_plural: str
    stats_csv: Path
    images_csv: Path
    placeholder_image: Path
    columns: List[str] | None  # None = use CSV headers as-is
    rename_map: Mapping[str, str] | None
    radar_stats: List[str]
    invert_rank_stats: List[str]
    rating_weights: Mapping[str, float]
    volume_stat: str  # used to sort season leaders
    radar_offset: float
    image_size: tuple[int, int]
    placeholder_size: tuple[int, int]
    radar_blurb: str
    season_checkbox_label: str
    season_caption: str


PASSING = CategoryConfig(
    key="passing",
    label="Passers (QB)",
    noun_plural="Quarterbacks",
    stats_csv=REPO_ROOT / "CSV_Files" / "NFL_QB" / "NFL_QB_Search.csv",
    images_csv=REPO_ROOT / "CSV_Files" / "NFL_QB" / "NFL_QB_Search_Images.csv",
    placeholder_image=REPO_ROOT / "Placeholder_Images" / "qb_playerholder_img.jpg",
    columns=None,
    rename_map={
        "Games Played": "GP",
        "Games Started": "GS",
        "Passes Completed": "Cmp",
        "Passes Attempted": "Att",
        "Completion Percentage": "Cmp%",
        "Passing Yards": "Yds",
        "Passing Touchdowns": "TD",
        "Touchdown Percentage": "TD%",
        "Interceptions": "INT",
        "Interceptions Percentage": "INT%",
        "Longest Pass": "Lng",
        "Yards Per Attempt": "Y/A",
        "Adjusted Yards Per Attempt": "AY/A",
        "Yards per Completion": "Y/C",
        "Yards Per Game": "Y/G",
        "Passer Rating": "Rating",
    },
    radar_stats=["Cmp%", "Yds", "TD", "TD%", "INT%", "Rating"],
    invert_rank_stats=["INT%"],
    rating_weights={
        "Cmp%": 10.0,
        "Yds": 10.0,
        "TD": 10.0,
        "TD%": 10.0,
        "INT%": 10.0,
        "Rating": 50.0,
    },
    volume_stat="Yds",
    radar_offset=3.141592653589793 / 6,
    image_size=(300, 406),
    placeholder_size=(344, 406),
    radar_blurb=(
        "Radar categories for passers: Cmp%, Pass Yds, Passing TDs, TD%, INT%, Rating. "
        "Taller wedges mean a stronger percentile rank that season."
    ),
    season_checkbox_label="Passing Stats",
    season_caption="Quarterbacks for the selected season (sorted by passing yards).",
)

RUSHING = CategoryConfig(
    key="rushing",
    label="Rushers (RB)",
    noun_plural="Running Backs",
    stats_csv=REPO_ROOT / "CSV_Files" / "NFL_RB" / "NFL_RB_Search.csv",
    images_csv=REPO_ROOT / "CSV_Files" / "NFL_RB" / "NFL_RB_Search_Images.csv",
    placeholder_image=REPO_ROOT / "Placeholder_Images" / "rb_playerholder_image.jpg",
    columns=None,
    rename_map=None,
    radar_stats=["Att", "Yards", "TD", "Y/A", "Y/G"],
    invert_rank_stats=[],
    rating_weights={
        "Att": 10.0,
        "Yards": 50.0,
        "TD": 20.0,
        "Y/A": 10.0,
        "Y/G": 10.0,
    },
    volume_stat="Yards",
    radar_offset=3.141592653589793 / 12,
    image_size=(300, 382),
    placeholder_size=(344, 382),
    radar_blurb=(
        "Radar categories for rushers: Att, Yards, TDs, Y/A, Y/G. "
        "Taller wedges mean a stronger percentile rank that season."
    ),
    season_checkbox_label="Rushing Stats",
    season_caption="Running backs for the selected season (sorted by rushing yards).",
)

RECEIVING = CategoryConfig(
    key="receiving",
    label="Receivers (WR/TE/RB)",
    noun_plural="Receivers",
    stats_csv=REPO_ROOT / "CSV_Files" / "NFL_WR" / "NFL_WR_Search.csv",
    images_csv=REPO_ROOT / "CSV_Files" / "NFL_WR" / "NFL_WR_Search_Images.csv",
    placeholder_image=REPO_ROOT / "Placeholder_Images" / "wr_playerholder_image.jpg",
    columns=None,
    rename_map=None,
    radar_stats=["Rec", "Yards", "TD", "Y/C", "Rec/G", "Y/G"],
    invert_rank_stats=[],
    rating_weights={
        "Rec": 15.0,
        "Yards": 40.0,
        "TD": 20.0,
        "Y/C": 10.0,
        "Rec/G": 5.0,
        "Y/G": 10.0,
    },
    volume_stat="Yards",
    radar_offset=3.141592653589793 / 6,
    image_size=(344, 433),
    placeholder_size=(344, 433),
    radar_blurb=(
        "Radar categories for receivers: Rec, Yards, TDs, Y/C, Rec/G, Y/G. "
        "Taller wedges mean a stronger percentile rank that season."
    ),
    season_checkbox_label="Receiving Stats",
    season_caption="Receivers for the selected season (sorted by receiving yards).",
)

CATEGORIES: Dict[str, CategoryConfig] = {
    PASSING.label: PASSING,
    RUSHING.label: RUSHING,
    RECEIVING.label: RECEIVING,
}
