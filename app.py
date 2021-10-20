import streamlit as st
import player_search_passing


st.set_page_config(
    page_title="NFL Player Search",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title('Pro Football Player Search')
st.sidebar.title('Pro Football Archives')


Pages = {"Passers (QB)": player_search_passing
        }
selection = st.sidebar.selectbox("Select One Of The Following Individual Categories",list(Pages.keys()))
page = Pages[selection]

if page:
    page.app()


    