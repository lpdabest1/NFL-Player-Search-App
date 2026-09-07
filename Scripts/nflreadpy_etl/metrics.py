"""Derived rate stats and NFL passer rating."""
from __future__ import annotations
import math
import numpy as np
import pandas as pd

def safe_div(num: pd.Series, den: pd.Series) -> pd.Series:
    den = den.replace(0, np.nan)
    return num / den

def round1(s: pd.Series) -> pd.Series:
    return s.round(1)

def as_nullable_int(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").round().astype("Int64")

def passer_rating(completions, attempts, yards, tds, ints) -> pd.Series:
    att = attempts.astype(float)
    cmp_ = completions.astype(float)
    yds = yards.astype(float)
    td = tds.astype(float)
    intercept = ints.astype(float)
    a = (((cmp_ / att) - 0.3) * 5).clip(0, 2.375)
    b = (((yds / att) - 3) * 0.25).clip(0, 2.375)
    c = ((td / att) * 20).clip(0, 2.375)
    d = (2.375 - ((intercept / att) * 25)).clip(0, 2.375)
    rating = ((a + b + c + d) / 6.0) * 100.0
    return rating.where(att > 0).round(1)

def season_age(birth_date: pd.Series, season: int) -> pd.Series:
    ref = pd.Timestamp(year=season, month=9, day=1)
    bd = pd.to_datetime(birth_date, errors="coerce")
    days = (ref - bd).dt.days
    return (days / 365.25).apply(lambda x: int(math.floor(x)) if pd.notna(x) else np.nan)
