import streamlit as st
import mysql.connector
import pandas as pd


# Initialize connection.
# Uses st.cache to only run once.
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])
    
conn = init_connection()

# Perform query.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * FROM nfl_player_qb_search")


# Print results.
#for row in rows:
    #st.write(f"{row[0]} has a :{row[1]}:")

qb_data = pd.DataFrame(rows)
qb_data.columns = ['Player','Image_Url','Image','Team','Age','GP','GS','Record','Wins %','Cmp','Att','Cmp%','Yds','TD','TD%','INT','INT%','1D','Lng','Y/A','AY/A','Y/C','Y/G','Rating','QBR','Sck','Sck%','Yds Loss']


st.dataframe(qb_data)

sorted_unique_players = sorted(qb_data.Player.unique())


if st.sidebar.checkbox('Search'):
    user_input = st.selectbox('Select a player to search', sorted_unique_players)
    if user_input in qb_data.Player:
        selected_player = qb_data.loc[qb_data['Player']==user_input]
        st.dataframe(selected_player)

