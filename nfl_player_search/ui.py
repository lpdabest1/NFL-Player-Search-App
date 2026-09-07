"""Shared Streamlit page for a single offensive category."""

from __future__ import annotations

from io import BytesIO

import pandas as pd
import requests
import streamlit as st
from PIL import Image

from nfl_player_search.charts import player_radar_figure
from nfl_player_search.config import TEAM_COLORS, CategoryConfig
from nfl_player_search.data import load_category_frames, player_team_for_year, player_years
from nfl_player_search.ranking import (
    add_percentile_ranks,
    compute_player_ratings,
    player_rank_among,
    season_leaderboard_size,
)


INTRO = """
This app lets you search historical NFL offensive players by category.
Pick a player and season to see headshots (when available), a peer radar chart,
season/career tables, and a composite ranking among that season's leaders.

* **Libraries:** pandas, streamlit, numpy, matplotlib, pillow, requests
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/)
* **Coverage:** roughly 1960–2020 (bundled CSVs; not live)
"""


def render_category_page(config: CategoryConfig) -> None:
    """Render the full search UI for one category."""
    st.markdown(INTRO)

    stats, images = load_category_frames(config)
    players = sorted(stats["Player"].dropna().unique().tolist())
    player = st.selectbox("Select a player to search", players)

    years = list(reversed(player_years(stats, player)))
    if not years:
        st.warning("No season rows found for this player.")
        return
    year = st.selectbox("Select a Year", years)

    team = player_team_for_year(stats, player, int(year))
    col1, col2 = st.columns([1, 1])

    _render_player_image(col1, images, player, config)

    season_df = stats[stats["Year"] == year].copy()
    for stat in config.radar_stats:
        season_df[stat] = pd.to_numeric(season_df[stat], errors="coerce")

    # Sort by volume so the leaderboard pool is meaningful
    season_df = season_df.sort_values(config.volume_stat, ascending=False)

    ranked = add_percentile_ranks(
        season_df[["Player", "Team"] + list(config.radar_stats)],
        config.radar_stats,
        invert=config.invert_rank_stats,
    )

    color = TEAM_COLORS.get(team, "blue")
    if team not in TEAM_COLORS:
        if st.sidebar.checkbox("Custom Color"):
            color = st.sidebar.color_picker("Pick a custom color for player chart", value="#1f77b4")
            st.sidebar.info(
                "Team color not found for this franchise name — pick a custom radar color."
            )

    if player in set(ranked["Player"]):
        fig = player_radar_figure(
            ranked,
            player,
            config.radar_stats,
            config.radar_offset,
            color,
        )
        col2.pyplot(fig)
        col2.write(config.radar_blurb)
    else:
        col2.warning("Not enough numeric stats to draw a radar for this selection.")

    career = stats.loc[stats["Player"] == player]
    season_row = career.loc[career["Year"] == year]
    st.markdown(f"{player} {year} Stats")
    st.dataframe(season_row, width="stretch")

    if st.sidebar.checkbox("Career"):
        st.subheader(f"{player} Career Stats")
        st.dataframe(career, width="stretch")

    pool_n = season_leaderboard_size(int(year))
    leaders = ranked.head(pool_n).copy()
    ratings = compute_player_ratings(leaders, config.rating_weights)

    if st.sidebar.checkbox(f"{config.season_checkbox_label} {year} Season"):
        st.caption(config.season_caption)
        st.dataframe(leaders, width="stretch")

    if st.sidebar.checkbox("Rankings"):
        _render_rating_bands(ratings, config.noun_plural, int(year))

    rank, pool = player_rank_among(ratings, player)
    if rank > 0:
        col1.success(
            f"{player} ranked {rank} out of {pool} qualifying {config.noun_plural} "
            f"during the {year} season."
        )
    else:
        col1.error(f"Not enough data to be ranked for the {year} season.")


def _render_player_image(col, images: pd.DataFrame, player: str, config: CategoryConfig) -> None:
    has_image = images["Player"].isin([player]).any()
    if has_image:
        urls = images.loc[images["Player"] == player, "Player Image"]
        for url in urls:
            try:
                resp = requests.get(str(url), timeout=10)
                resp.raise_for_status()
                img = Image.open(BytesIO(resp.content)).resize(config.image_size)
                col.image(img, caption=player)
                return
            except Exception:
                continue
    if config.placeholder_image.exists():
        img = Image.open(config.placeholder_image).resize(config.placeholder_size)
        col.image(img, caption=player)
    else:
        col.info("No player image available.")


def _render_rating_bands(ratings: pd.DataFrame, noun_plural: str, year: int) -> None:
    if 1960 <= year < 1970:
        left, right = st.columns(2)
        left.subheader(f"Top 10 Rated {noun_plural}")
        left.dataframe(ratings.head(10), width="stretch")
        right.subheader(f"Bottom 10 Rated {noun_plural}")
        right.dataframe(ratings.tail(10), width="stretch")
        return

    top, mid, bottom = st.columns(3)
    top.subheader(f"Top 10 Rated {noun_plural}")
    top.dataframe(ratings.head(10), width="stretch")
    mid.subheader(f'"Middle Of The Pack" Rated {noun_plural}')
    mid.dataframe(ratings.iloc[10:22], width="stretch")
    bottom.subheader(f"Bottom 10 Rated {noun_plural}")
    bottom.dataframe(ratings.tail(10), width="stretch")
