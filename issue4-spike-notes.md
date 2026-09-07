# Issue #4 spike notes — headshot refresh + missing-image UX

Date: 2026-09-07 (America/Chicago)

## HTTP 200 sample (~50 modern players)
- Source: `nflreadpy.load_player_stats(2021–2025, summary_level="reg")` → `headshot_url`
- Sample: 50 players (QB/RB/TE mix, seasons ≥2023) with non-null URLs
- Result: **50/50 HTTP 200** against `static.www.nfl.com` (HEAD then GET fallback)
- Modern skill-position non-null `headshot_url` rate on unique `player_id`: **~99.7%**

## Join keys
- Stats `player_id` **==** players `gsis_id` (confirmed on samples)
- Prefer map keyed by **`gsis_id` / `player_id`**
- Emit UI join on **display `Player`** matching Search / season_data names (`player_display_name`)
- Name collision risk: rare (e.g. two “Josh Johnson” gsis_ids in modern window); resolve via latest season’s `player_id` from stats
- Trailing spaces in a few historical CSV names can miss exact match — strip for lookup, emit original stats `Player` string

## Coverage vs app player universe (exact name join)
| Category | Unique Players | Matched + URL | Modern (Year≥2021) URL |
|----------|----------------|---------------|-------------------------|
| QB       | ~1738          | ~87.6%        | **100%**                |
| RB       | ~4983          | ~88.8%        | **100%**                |
| WR       | ~5975          | ~89.8%        | **~99.7%**              |

Gaps are mostly pre-nflverse / obscure names (e.g. Johnny Unitas, Gale Sayers, Bart Starr). Historical gaps are **acceptable** per decide-doc.

## Brandon Jacobs
- Previously missing from RB **images** CSV (only Josh Jacobs present) while present in RB **stats**
- `load_players()` has gsis `00-0023545` + working NFL.com headshot (**HTTP 200**)
- After refresh, Jacobs is a **hit**, not a miss — use **Johnny Unitas** (or any unmatched historical) for “Image unavailable” smoke

## CSV vs embed decision
- One row per unique `Player` with a URL; schema **`Player,Player Image`**
- Estimated size well under existing PFR image CSVs (which duplicated per-year / stale PFR URLs)
- **Decision: plain CSV refresh** under `CSV_Files/NFL_{QB,RB,WR}/` — no embed chunks needed (unlike #6 season payloads)

## UX
- Stop silent silhouette-as-photo
- On no URL / all fetches fail → placeholder silhouette **plus** explicit **“Image unavailable”**
- Ranking / radar untouched

## Out of scope (confirmed)
- Live Cloud scrape / runtime nflverse fetch
- PFR re-scrape
- Guaranteeing 1960–1998 headshots
