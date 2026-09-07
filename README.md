# NFL Player Search App

Streamlit app for searching historical NFL offensive players (QB / RB / WR-TE) and exploring season and career stats with peer radar charts and composite rankings.

Originally built as a post-college learning project; this branch modernizes the structure and tooling while keeping the Streamlit UX.

## Features

- Browse **Passers**, **Rushers**, and **Receivers**
- Player + season selectors
- Headshot (when scraped) or placeholder image
- Matplotlib radar chart vs season peers (team-colored when possible)
- Season table, optional career table, season leaderboard, and composite rankings

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
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
Scripts/                  # Original scraping / data scripts (unchanged)
Playersearch/             # Legacy-compatible thin entry (prefer streamlit_app.py)
tests/                    # Unit tests for pure logic
Procfile / setup.sh       # Heroku-style Streamlit deploy helpers
```

## Data

- Source: [pro-football-reference.com](https://www.pro-football-reference.com/)
- Bundled CSVs cover roughly **1960–2020**
- Data is offline and static in this repo — refreshing seasons is a separate follow-up

## Deploy

`Procfile` runs:

```text
web: sh setup.sh && streamlit run streamlit_app.py
```

## Known limitations

- Stats are not live; recent seasons after the bundled CSVs are missing
- Franchise naming in older rows may not match modern team-color keys (custom color picker available)
- Image URLs depend on third-party hosting availability
