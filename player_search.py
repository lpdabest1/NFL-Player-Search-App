import streamlit as st
import mysql.connector
import pandas as pd
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import requests
# Initialize connection.
# Uses st.cache to only run once.
@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])
    
conn = init_connection()

# Perform query.
# Uses st.cache to only rerun when the query changes or after 10 min.
@st.cache(ttl=600)
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

#qb_data[qb_data['Player'] == 'Tom Brady']
#st.dataframe(qb_data)

#qb_data = qb_data.astype(dtype={'Player': 'string'})


#edited_qb_data = qb_data

#edited_qb_data['Player'] = qb_data['Player'].str.split(',')
#edited_qb_data['Image_Url'] = qb_data['Image_Url'].str.split(',')
#edited_qb_data['Team'] = qb_data['Team'].str.split(',')
data_types = qb_data.dtypes                   
#print(data_types)


sorted_unique_players = sorted(qb_data.Player.unique())

user_input = st.selectbox('Select a player to search', sorted_unique_players)

# Two Columns (one for image and one for data)
col1, col2= st.columns([1,1])
if user_input:
    player_image = qb_data.loc[qb_data['Player']== user_input, ['Image_Url']]
    for i in player_image.Image_Url:
        get_url = requests.get(i)
        img = Image.open(BytesIO(get_url.content))
        col1.image(img, width=250, caption=user_input)







#qb_data.rename(columns={'Completion Percentage': 'Cmp%',
#'Passing Yards': 'Pass Yds', 'Passing Touchdowns':'Pass TD','Touchdown Percentage':'TD%','Interceptions Percentage':'INT%'}, inplace= True)
#print(df)

#   Naveen Venkatesan --> Data Scientist url:https://towardsdatascience.com/scraping-nfl-stats-to-compare-quarterback-efficiencies-4989642e02fe
#   This is where I found a template for how to generate radar charts for comparing nfl quarterbacks
# Stat Categories
# Cmp%, Pass Yds, Passing TDs, TD%, INT, INT%, QBR

#stat_categories = ['Completion Percentage','Passing Yards','Passing Touchdowns','Touchdown Percentage','Interceptions','QBR']
stat_categories = ['Cmp%','Yds','TD','TD%','INT%','Rating']
#stats_data_categories_rankings = df['Cmp%','Pass Yds','Pass TD','TD%','INT','QBR']

stats_data_categories = qb_data[['Player','Team'] + stat_categories] 

# Convert data to numerical values
for i in stat_categories:
    stats_data_categories[i] = pd.to_numeric(qb_data[i])

#Displaying new DataFrame that will be used for analyzing stats for radar charts
#st.dataframe(stats_data_categories)

# Create rankings for stat categories
for i in stat_categories:
    stats_data_categories[i + ' Rank'] = stats_data_categories[i].rank(pct=True)

# reverse the stats of ascension sort for interceptions stat category
stats_data_categories['INT% Rank'] = (1 - stats_data_categories['INT% Rank'])

# Viewing our updated stats DataFrame
#print(stats_data_categories.head)

# General plot parameters for radar chart
#mpl.rcParams['font.family'] = 'Avenir'
mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.linewidth'] = 0
mpl.rcParams['xtick.major.pad'] = 15

# Hex Codes for the NFL Teams, which will be stored
team_colors = {'Arizona Cardinals':'#97233f', 'Atlanta Falcons':'#a71930', 'Baltimore Ravens':'#241773', 'Buffalo Bills':'#00338d', 'Carolina Panthers':'#0085ca',
            'Chicago Bears':'#0b162a', 'Cincinnati Bengals':'#fb4f14', 'Cleveland Browns':'#311d00', 'Dallas Cowboys':'#041e42', 'Denver Broncos':'#002244', 
            'Detroit Lions':'#0076b6', 'Green Bay Packers':'#203731', 'Houston Texans':'#03202f', 'Indianapolis Colts':'#002c5f', 'Jacksonville Jaguars':'#006778', 
            'Kansas City Chiefs':'#e31837', 'Los Angeles Chargers':'#002a5e', 'Los Angeles Rams':'#003594', 'Miami Dolphins':'#008e97', 
            'Minnesota Vikings':'#4f2683', 'New England Patriots':'#002244', 'New Orleans Saints':'#d3bc8d', 'New York Giants':'#0b2265', 
            'New York Jets':'#125740', 'Las Vegas Raiders':'#000000', 'Philadelphia Eagles':'#004c54', 'Pittsburgh Steelers':'#ffb612', 
            'San Francisco 49ers':'#aa0000', 'Seattle Seahawks':'#002244', 'Tampa Bay Buccaneers':'#d50a0a', 'Tennessee Titans':'#0c2340', 'Washington Football Team':'#773141'}

# Calculate angles for radar chart
offset = np.pi/6
angles = np.linspace(0, 2*np.pi, len(stat_categories) + 1) + offset


def create_radar_chart(ax, angles, player_data, color='blue'):
    # Plot data and fill with team color
    ax.plot(angles, np.append(player_data[-(len(angles)-1):], player_data[-(len(angles)-1)]), color=color, linewidth=2)
    ax.fill(angles, np.append(player_data[-(len(angles)-1):], player_data[-(len(angles)-1)]), color=color, alpha=0.2)

    # Set category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(stat_categories)

    # Remove radial labels
    ax.set_yticklabels([])

    # Add player name
    ax.text(np.pi/2, 1.7, player_data[0], ha='center', va='center', size=18, color=color)


    # Use white grid
    ax.grid(color='white', linewidth=1.5)

    # Set axis limits
    ax.set(xlim=(0, 2*np.pi), ylim=(0, 1))

    return ax

# Function to get QB data
def get_qb_data(data, team):
    return np.asarray(data[data['Team'] == team])[0]

def get_qb_player_data(data, player):
    return np.asarray(data[data['Player'] == player])[0]


# ******************User Input for customized Radar Chart ****************************
# Sidebar User Options based on selected team and player
#sorted_unique_players_ = sorted(stats_data_categories.Player.unique())


#col3.title('Performance Chart')
#col3.info('A Chart that visualizes how big ben did compared to his peers for the 2020 season')


# Created Figure for Player ###########################################################################################################
#col3.subheader('Player Search:')
#user_input_demo_player_ = st.sidebar.selectbox('Player(s):', sorted_unique_players_)


# Unique Player Create Figure
fig_player = plt.figure(figsize=(8, 8), facecolor='white')# Add subplots
ax2 = fig_player.add_subplot(222, projection='polar', facecolor='#ededed')
data_demo_player = get_qb_player_data(stats_data_categories, user_input)# Plot QB data



if user_input:
    if st.sidebar.checkbox('Custom Color'):
        custom_color = st.sidebar.text_input("Enter a custom color for chart")
        st.sidebar.info('You can type in a color to customize the radar chart to your liking. Blue, Teal, Red perhaps? Just enter it to give it a try. Note: The default color is blue if text is left empty.')
        if not custom_color:
            default = 'blue'
            custom_color=default
        ax2 = create_radar_chart(ax2, angles, data_demo_player, color=custom_color)
    else:
        ax2 = create_radar_chart(ax2, angles, data_demo_player)
    col2.pyplot(fig_player)
    col2.write('As displayed above, the main points of emphasis that I have selected to compare for the quarterbacks in regards to the passing game are: Cmp%, Pass Yds, Passing TDs, TD%, INT, INT%, QBR. The greater the height and shape of one category, the better the player was in that category.')
    
    # DataFrame for Team Passing Rankings
    Player_Ranks_df = stats_data_categories.loc[stats_data_categories['Player']==user_input]
    st.subheader(user_input + ' Passing Stats W/ Ranking Percent Per Category')
    st.dataframe(Player_Ranks_df)





#for i in qb_data['Player']:
#   if user_input == i:
#        selected_player = qb_data.loc[qb_data['Player']==user_input]
            #selected_player = qb_data[qb_data['Team'] == user_input]
        #col2.dataframe(selected_player)
    