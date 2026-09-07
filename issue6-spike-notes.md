# Issue #6 spike notes — nflreadpy ETL (2021–present)

Date: 2026-09-06 (America/Chicago)

## Environment
- `nflreadpy` 0.1.5 → Polars DataFrames (`.to_pandas()`)
- `get_current_season()` = **2025**, `get_current_week()` = **22** → treat 2025 REG as completed; append **2021–2025**

## Primary source
```python
nfl.load_player_stats(seasons, summary_level="reg")
```
Key fields: `player_id`, `player_display_name`, `position`, `recent_team`, `season`, `games`,
`completions`, `attempts`, `passing_yards`, `passing_tds`, `passing_interceptions`,
`carries`, `rushing_yards`, `rushing_tds`, `rushing_fumbles`,
`receptions`, `receiving_yards`, `receiving_tds`, `headshot_url`

Filter out null `player_display_name` (orphan rows with absurd `games`, e.g. 272).

## Lng / Long / Longest Pass
- **Not present** on seasonal or weekly `load_player_stats` (only distance buckets like `passing_40`).
- **Resolved via PBP:** `load_pbp(season)` → max `yards_gained` by:
  - passer (`complete_pass==1`) → Longest Pass
  - rusher (`rush_attempt==1`) → Long
  - receiver (`complete_pass==1`) → Long
- Spot-check 2024: Levis 98, Darnold 97, etc. look plausible.

## Age
- Not on seasonal stats.
- Join `load_players()` on `gsis_id` / `player_id`; use `birth_date` (better coverage than weekly rosters).
- Age ≈ floor years from birth_date to **Sept 1 of season year** (PFR-ish season age).
- Nullable if birth_date missing.

## Games Started
- Not on seasonal stats / snap counts.
- **Approx from** `load_depth_charts(season)`: count distinct REG weeks 1–18 where `depth_team == 1`.
- Clip GS ≤ Games Played. **2025 GS blank** (depth-chart schema change).

## Team map
- Stats use abbrev in `recent_team`.
- `load_teams()` → `team_abbr` / `team_name` (full names).
- Prefer modern full names matching UI `TEAM_COLORS` (e.g. Las Vegas Raiders, Los Angeles Chargers/Rams, Washington Commanders).
- Note: historical CSVs still say "Washington Football Team" for 2020; 2022+ should be Commanders. Add Commanders to `TEAM_COLORS`.

## Passer rating spot-check
NFL formula implemented; Tom Brady 2021 (485/719, 5316 yds, 43 TD, 12 INT) → **102.1** (PFR ~102.1). AY/A classic `(Yds+20*TD-45*INT)/Att` → 7.8.

## Inclusion filters (match PFR-style tables)
| CSV | Filter | 2020 nflverse vs hist |
|-----|--------|------------------------|
| QB  | `attempts > 0` | 112 vs 112 |
| RB  | `carries > 0` | 372 vs 364 |
| WR  | `receptions > 0` (WR/TE/RB + anyone with a catch) | 499 vs 486 |

Close enough; slight diffs expected (nflverse vs PFR scoring).

## Fumbles (RB)
Use `rushing_fumbles` (not lost-only). Henry 2020: nflverse 3 == hist 3.

## Idempotency
Drop existing CSV rows with `Year >= 2021`, then concat historical + new; preserve exact header order.

## Out of scope
- Image CSV refresh / headshots (#4) — `headshot_url` available on stats if needed later
- Rewriting 1960–2020 rows
- Runtime Cloud fetch

## Post-implement notes
- Age: switched to `load_players().birth_date` (near-100% coverage) vs weekly rosters (~58%).
- GS: depth charts weeks 1–18 only (week 19 sometimes mis-tagged REG); clip GS ≤ GP; **2025 GS blank** (schema change).
- Lng via PBP max `yards_gained`; QB Longest Pass still ~13% NaN (attempt-only / no completion).
- Seasons appended: **2021–2025**.
