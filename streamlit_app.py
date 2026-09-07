"""Entrypoint for the NFL Player Search Streamlit app.

Run from the repository root:

    streamlit run streamlit_app.py
"""

from __future__ import annotations

import streamlit as st

from nfl_player_search.config import CATEGORIES
from nfl_player_search.ui import render_category_page

st.set_page_config(
    page_title="NFL Player Search",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Pro Football Player Search")
st.sidebar.title("Pro Football Archives")

selection = st.sidebar.selectbox(
    "Select One Of The Following Offensive Categories",
    list(CATEGORIES.keys()),
)
render_category_page(CATEGORIES[selection])
