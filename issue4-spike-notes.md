# Issue #4 spike notes — headshot URL refresh + missing-image UX

Date: 2026-09-07 (America/Chicago)

## Environment
- `nflreadpy` 0.1.5; `get_current_season()`=2025, `get_current_week()`=22
- Sample season for hit-rate: **2024 REG** player_stats

## Join keys
- Stats `player_id` **equals** `load_players().gsis_id` (200/200 sample matched)
- Prefer **gsis_id** map for URLs; emit UI `Player` via `player_display_name` / `display_name` so `images["Player"].isin([player])` still works
- Display-name collisions (multi-gsis) are rare (~197 across 1999–2025); resolve by position preference + latest season + non-null URL

## 2024 non-null `headshot_url` (position filters same as #6 ETL)
| Pos | with URL / unique players | rate |
|-----|---------------------------|------|
| QB  | 103/103 | **100%** |
| RB  | 333/333 | **100%** |
| WR  | 470/470 | **100%** |

`load_players().headshot` also ~99.3% non-null; stats URL preferred when both exist (NFL.com CDN).

## HTTP check (~21 sample URLs)
- User-Agent set; require `Content-Type: image/*`, body >500 bytes, reject HTML disguises
- Result: **21/21 good** (PNG from `static.www.nfl.com`)

## Name match vs app stats (hist CSV + season_data)
Using `display_name`/`player_display_name` → gsis → URL (players.headshot ∪ stats headshot_url):

| Pos | overall URL rate | modern (≥2021) |
|-----|------------------|----------------|
| QB  | ~87–88% | **100%** |
| RB  | ~88–89% | **100%** |
| WR  | ~89–90% | **~99.8%** |

Era gaps (expected): 1960–1979 ~3% URL; 1980–1998 ~23–28%; 1999+ strong.

## Known miss
- **Brandon Jacobs**: present in RB stats CSV, absent from old images CSV → expect silhouette + **Image missing** after UX change (may still lack nflverse URL depending on roster coverage)

## Decisions locked for implement
1. Remap via nflreadpy — **no PFR scrape**
2. Commit refreshed `*_Search_Images.csv` (`Player`,`Player Image`); nflreadpy stays in requirements-dev only
3. UX: failed/missing URL → silhouette **plus** `st.caption("Image missing")`
4. Optional hardening: User-Agent + reject non-image bodies
