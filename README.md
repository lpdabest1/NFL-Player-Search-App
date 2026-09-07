# NFL Player Search App

Streamlit app for searching historical NFL offensive players (QB / RB / WR-TE) and exploring season and career stats with peer radar charts and composite rankings.

Originally built as a post-college learning project; this branch modernizes the structure and tooling while keeping the Streamlit UX.

## Features

- Browse **Passers**, **Rushers**, and **Receivers** via `st.navigation` + segmented control
- Player/year filters run inside `@st.fragment` so chart updates avoid a full-app rerun
- Player + season selectors
- Headshot (nflverse URL when available) or silhouette + **Image missing** label
- Matplotlib radar chart vs season peers (team-colored when possible)
- Season table, optional career table, season leaderboard, and composite rankings

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Run tests:

```bash
pip install -r requirements-dev.txt
pytest
```

## Project layout

```
streamlit_app.py          # App entrypoint
nfl_player_search/        # Shared package (config, data, ranking, charts, UI)
CSV_Files/                # Bundled historical stats + image URLs
Placeholder_Images/       # Fallback headshots
Scripts/                  # Scraping / ETL scripts
Playersearch/             # Legacy-compatible thin entry (prefer streamlit_app.py)
tests/                    # Unit tests for pure logic
Procfile / setup.sh       # Heroku-style Streamlit deploy helpers
```

## Data

- Historical rows (roughly **1960–2020**) came from [pro-football-reference.com](https://www.pro-football-reference.com/)
- Seasons **2021–present** are built offline via [`nflreadpy`](https://github.com/nflverse/nflreadpy) and committed as embedded zlib+base64 payloads in `nfl_player_search/season_data/` (merged at load time so historical base CSVs stay unchanged)
- Streamlit Cloud reads only committed files (no live nflverse fetch at runtime)

### Refresh seasons (dev / ETL)

```bash
pip install -r requirements-dev.txt
python Scripts/etl_nflreadpy_append.py
# optional: python Scripts/etl_nflreadpy_append.py --start 2021 --end 2025
```

The ETL drops any existing `Year >= 2021` rows, rebuilds 2021→latest completed regular season from nflreadpy, rewrites Search CSVs, and regenerates `nfl_player_search/season_data/*_chunk_*.py`.

### Refresh headshots (dev / ETL)

```bash
pip install -r requirements-dev.txt
python Scripts/etl_nflreadpy_headshots.py
# optional: python Scripts/etl_nflreadpy_headshots.py --stats-start 1999 --stats-end 2025
```

Rebuilds `CSV_Files/NFL_{QB,RB,WR}/*_Search_Images.csv` (`Player`,`Player Image`) by joining stats display names to nflverse **`gsis_id`** and taking `headshot_url` / `headshot`. Prefer gsis over fuzzy names; thin pre-~1999 coverage is expected. No PFR scrape; URLs are committed for Cloud (no runtime nflverse fetch).

## Deploy

`Procfile` runs:

```text
web: sh setup.sh && streamlit run streamlit_app.py
```

## Known limitations

- Stats are offline snapshots; re-run the ETL and commit season_data modules to pick up a new season
- Games Started for 2025+ may be blank (nflverse depth-chart schema change); Age/Lng use players + PBP joins
- Franchise naming in older rows may not match modern team-color keys (custom color picker available)
- Pre-~1999 / obscure careers may show silhouette + “Image missing” (nflverse headshot coverage is modern-leaning)
