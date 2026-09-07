"""Build QB/RB/WR frames matching committed CSV schemas."""
from __future__ import annotations
import pandas as pd
from .constants import QB_HEADERS, RB_HEADERS, WR_HEADERS
from .metrics import as_nullable_int, passer_rating, round1, safe_div

def attach_common(df, team_map, ages, gs):
    out = df.copy()
    out["Player"] = out["player_display_name"]
    out["Team"] = out["recent_team"].map(team_map).fillna(out["recent_team"])
    out["Year"] = out["season"].astype(int)
    out["Games Played"] = out["games"]
    out = out.merge(ages, on=["player_id", "season"], how="left")
    out = out.merge(gs, on=["player_id", "season"], how="left")
    seasons_with_gs = set(gs["season"].unique()) if len(gs) else set()
    mask = out["season"].isin(seasons_with_gs) & out["Games Started"].isna()
    out.loc[mask, "Games Started"] = 0
    both = out["Games Started"].notna() & out["Games Played"].notna()
    out.loc[both, "Games Started"] = out.loc[both, ["Games Started", "Games Played"]].min(axis=1)
    return out

def build_qb(stats, team_map, ages, gs, pass_lng):
    df = stats[stats["attempts"].fillna(0) > 0].copy()
    df = attach_common(df, team_map, ages, gs)
    df = df.merge(pass_lng, on=["player_id", "season"], how="left")
    att = df["attempts"].astype(float)
    cmp_ = df["completions"].astype(float)
    yds = df["passing_yards"].astype(float)
    td = df["passing_tds"].astype(float)
    intercept = df["passing_interceptions"].astype(float)
    gp = df["Games Played"].astype(float)
    df["Passes Completed"] = df["completions"].fillna(0).astype(int)
    df["Passes Attempted"] = df["attempts"].fillna(0).astype(int)
    df["Completion Percentage"] = round1(100 * safe_div(cmp_, att))
    df["Passing Yards"] = df["passing_yards"].fillna(0).astype(int)
    df["Passing Touchdowns"] = df["passing_tds"].fillna(0).astype(int)
    df["Touchdown Percentage"] = round1(100 * safe_div(td, att))
    df["Interceptions"] = df["passing_interceptions"].fillna(0).astype(int)
    df["Interceptions Percentage"] = round1(100 * safe_div(intercept, att))
    df["Yards Per Attempt"] = round1(safe_div(yds, att))
    df["Adjusted Yards Per Attempt"] = round1(safe_div(yds + 20 * td - 45 * intercept, att))
    df["Yards per Completion"] = round1(safe_div(yds, cmp_))
    df["Yards Per Game"] = round1(safe_div(yds, gp))
    df["Passer Rating"] = passer_rating(cmp_, att, yds, td, intercept)
    df["Age"] = as_nullable_int(df["Age"])
    df["Games Started"] = as_nullable_int(df["Games Started"])
    df["Games Played"] = as_nullable_int(df["Games Played"])
    return df[QB_HEADERS].sort_values(["Year", "Passing Yards"], ascending=[True, False])

def build_rb(stats, team_map, ages, gs, rush_lng):
    df = stats[stats["carries"].fillna(0) > 0].copy()
    df = attach_common(df, team_map, ages, gs)
    df = df.merge(rush_lng, on=["player_id", "season"], how="left")
    att = df["carries"].astype(float)
    yds = df["rushing_yards"].astype(float)
    gp = df["Games Played"].astype(float)
    df["Att"] = df["carries"].fillna(0).astype(int)
    df["Yards"] = df["rushing_yards"].fillna(0).astype(int)
    df["TD"] = df["rushing_tds"].fillna(0).astype(int)
    df["Y/A"] = round1(safe_div(yds, att))
    df["Y/G"] = round1(safe_div(yds, gp))
    df["Fumbles"] = df["rushing_fumbles"].astype(float)
    df["Age"] = as_nullable_int(df["Age"])
    df["Games Started"] = as_nullable_int(df["Games Started"])
    df["Games Played"] = as_nullable_int(df["Games Played"])
    return df[RB_HEADERS].sort_values(["Year", "Yards"], ascending=[True, False])

def build_wr(stats, team_map, ages, gs, rec_lng):
    df = stats[stats["receptions"].fillna(0) > 0].copy()
    df = attach_common(df, team_map, ages, gs)
    df = df.merge(rec_lng, on=["player_id", "season"], how="left")
    rec = df["receptions"].astype(float)
    yds = df["receiving_yards"].astype(float)
    gp = df["Games Played"].astype(float)
    df["Rec"] = df["receptions"].fillna(0).astype(int)
    df["Yards"] = df["receiving_yards"].fillna(0).astype(int)
    df["Y/C"] = round1(safe_div(yds, rec))
    df["TD"] = df["receiving_tds"].fillna(0).astype(int)
    df["Rec/G"] = round1(safe_div(rec, gp))
    df["Y/G"] = round1(safe_div(yds, gp))
    df["Age"] = as_nullable_int(df["Age"])
    df["Games Started"] = as_nullable_int(df["Games Started"])
    df["Games Played"] = as_nullable_int(df["Games Played"])
    return df[WR_HEADERS].sort_values(["Year", "Yards"], ascending=[True, False])
