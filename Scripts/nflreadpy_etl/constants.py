"""Paths and CSV header contracts."""
from __future__ import annotations
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
QB_CSV = REPO_ROOT / "CSV_Files" / "NFL_QB" / "NFL_QB_Search.csv"
RB_CSV = REPO_ROOT / "CSV_Files" / "NFL_RB" / "NFL_RB_Search.csv"
WR_CSV = REPO_ROOT / "CSV_Files" / "NFL_WR" / "NFL_WR_Search.csv"
APPEND_FROM_YEAR = 2021

QB_HEADERS = [
    "Player", "Team", "Age", "Games Played", "Games Started",
    "Passes Completed", "Passes Attempted", "Completion Percentage",
    "Passing Yards", "Passing Touchdowns", "Touchdown Percentage",
    "Interceptions", "Interceptions Percentage", "Longest Pass",
    "Yards Per Attempt", "Adjusted Yards Per Attempt", "Yards per Completion",
    "Yards Per Game", "Passer Rating", "Year",
]
RB_HEADERS = [
    "Player", "Team", "Age", "Games Played", "Games Started",
    "Att", "Yards", "TD", "Long", "Y/A", "Y/G", "Fumbles", "Year",
]
WR_HEADERS = [
    "Player", "Team", "Age", "Games Played", "Games Started",
    "Rec", "Yards", "Y/C", "TD", "Long", "Rec/G", "Y/G", "Year",
]
