"""Entrypoint for the NFL Player Search Streamlit app.

Run from the repository root:

    streamlit run streamlit_app.py
"""

from __future__ import annotations

import streamlit as st

from nfl_player_search.config import PASSING, RECEIVING, RUSHING
from nfl_player_search.ui import render_category_page

st.set_page_config(
    page_title="NFL Player Search",
    layout="centered",
    initial_sidebar_state="expanded",
)


def _passers_page() -> None:
    render_category_page(PASSING)


def _rushers_page() -> None:
    render_category_page(RUSHING)


def _receivers_page() -> None:
    render_category_page(RECEIVING)


passers = st.Page(
    _passers_page,
    title="Passers (QB)",
    icon="🏈",
    url_path="passers",
    default=True,
)
rushers = st.Page(
    _rushers_page,
    title="Rushers (RB)",
    icon="🏃",
    url_path="rushers",
)
receivers = st.Page(
    _receivers_page,
    title="Receivers (WR/TE)",
    icon="🏆",
    url_path="receivers",
)

st.navigation(
    {
        "Pro Football Archives": [passers, rushers, receivers],
    }
).run()
