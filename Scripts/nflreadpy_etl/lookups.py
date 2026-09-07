"""Team map, age, games started, and longest-play lookups."""
from __future__ import annotations
from typing import Iterable
import pandas as pd
from .metrics import season_age

def latest_completed_season() -> int:
    import nflreadpy as nfl
    season = int(nfl.get_current_season())
    week = int(nfl.get_current_week())
    if week < 18:
        return season - 1
    return season

def build_team_map() -> dict[str, str]:
    import nflreadpy as nfl
    teams = nfl.load_teams().to_pandas()
    mapping = dict(zip(teams["team_abbr"], teams["team_name"]))
    mapping.setdefault("LA", mapping.get("LAR", "Los Angeles Rams"))
    return mapping

def load_age_lookup(seasons: Iterable[int]) -> pd.DataFrame:
    import nflreadpy as nfl
    players = nfl.load_players().to_pandas()
    players = players.dropna(subset=["gsis_id"]).drop_duplicates("gsis_id")
    frames = []
    for season in seasons:
        part = players[["gsis_id", "birth_date"]].copy()
        part["season"] = season
        part["Age"] = season_age(part["birth_date"], season)
        frames.append(part[["gsis_id", "season", "Age"]].rename(columns={"gsis_id": "player_id"}))
    if not frames:
        return pd.DataFrame(columns=["player_id", "season", "Age"])
    return pd.concat(frames, ignore_index=True)

def load_gs_lookup(seasons: Iterable[int]) -> pd.DataFrame:
    import nflreadpy as nfl
    frames = []
    for season in seasons:
        try:
            dc = nfl.load_depth_charts([season]).to_pandas()
        except Exception as exc:  # noqa: BLE001
            print(f"  warning: depth charts {season}: {exc}")
            continue
        if dc.empty or "gsis_id" not in dc.columns:
            continue
        if "game_type" not in dc.columns or "week" not in dc.columns or "depth_team" not in dc.columns:
            print(f"  warning: depth charts {season} lack weekly starter fields; GS skipped")
            continue
        dc = dc[
            (dc["game_type"] == "REG")
            & (dc["week"].fillna(0) <= 18)
            & (dc["depth_team"].astype(str) == "1")
        ].copy()
        dc["season"] = season
        gs = (
            dc.dropna(subset=["gsis_id"])
            .groupby(["gsis_id", "season"], as_index=False)["week"]
            .nunique()
            .rename(columns={"gsis_id": "player_id", "week": "Games Started"})
        )
        frames.append(gs)
    if not frames:
        return pd.DataFrame(columns=["player_id", "season", "Games Started"])
    return pd.concat(frames, ignore_index=True)

def load_long_lookups(seasons: Iterable[int]):
    import nflreadpy as nfl
    pass_frames, rush_frames, rec_frames = [], [], []
    for season in seasons:
        print(f"  PBP longest plays {season}...")
        pbp = nfl.load_pbp([season]).to_pandas()
        if pbp.empty:
            continue
        if "season_type" in pbp.columns:
            pbp = pbp[pbp["season_type"] == "REG"]
        if "complete_pass" in pbp.columns and "passer_player_id" in pbp.columns:
            comp = pbp[(pbp["complete_pass"] == 1) & pbp["passer_player_id"].notna()]
            pl = (
                comp.groupby(["passer_player_id", "season"], as_index=False)["yards_gained"]
                .max()
                .rename(columns={"passer_player_id": "player_id", "yards_gained": "Longest Pass"})
            )
            pass_frames.append(pl)
        if "rush_attempt" in pbp.columns and "rusher_player_id" in pbp.columns:
            rush = pbp[(pbp["rush_attempt"] == 1) & pbp["rusher_player_id"].notna()]
            rl = (
                rush.groupby(["rusher_player_id", "season"], as_index=False)["yards_gained"]
                .max()
                .rename(columns={"rusher_player_id": "player_id", "yards_gained": "Long"})
            )
            rush_frames.append(rl)
        if "complete_pass" in pbp.columns and "receiver_player_id" in pbp.columns:
            rec = pbp[(pbp["complete_pass"] == 1) & pbp["receiver_player_id"].notna()]
            rcl = (
                rec.groupby(["receiver_player_id", "season"], as_index=False)["yards_gained"]
                .max()
                .rename(columns={"receiver_player_id": "player_id", "yards_gained": "Long"})
            )
            rec_frames.append(rcl)
    empty_pass = pd.DataFrame(columns=["player_id", "season", "Longest Pass"])
    empty_long = pd.DataFrame(columns=["player_id", "season", "Long"])
    pass_lng = pd.concat(pass_frames, ignore_index=True) if pass_frames else empty_pass
    rush_lng = pd.concat(rush_frames, ignore_index=True) if rush_frames else empty_long
    rec_lng = pd.concat(rec_frames, ignore_index=True) if rec_frames else empty_long
    return pass_lng, rush_lng, rec_lng

def load_seasonal_stats(seasons: list[int]) -> pd.DataFrame:
    import nflreadpy as nfl
    stats = nfl.load_player_stats(seasons, summary_level="reg").to_pandas()
    stats = stats[stats["player_display_name"].notna()].copy()
    if "season_type" in stats.columns:
        stats = stats[stats["season_type"] == "REG"]
    return stats
