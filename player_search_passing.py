from collections import UserList
from numpy.lib.function_base import select
import streamlit as st
import pandas as pd
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import requests

def app():
    
    st.markdown("""
        This app performs a player search with respect to the offensive category selected on the sidebar. You can view the player's career, specific season you select, as well as how they performed that season in that category compared to their peers!
        In addition, you can also take a look at the stats for that season for all the players in that category.
        * **Python libraries:** pandas, streamlit, numpy, matplotlib, pillow, beautifulsoup4, BytesIO
        * **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
        Data is from 1960 to 2020.
    """)




    # Hex Codes for the NFL Teams, which will be stored
    team_colors = {'Arizona Cardinals':'#97233f', 'Atlanta Falcons':'#a71930', 'Baltimore Ravens':'#241773', 'Buffalo Bills':'#00338d', 'Carolina Panthers':'#0085ca',
                'Chicago Bears':'#0b162a', 'Cincinnati Bengals':'#fb4f14', 'Cleveland Browns':'#311d00', 'Dallas Cowboys':'#041e42', 'Denver Broncos':'#002244', 
                'Detroit Lions':'#0076b6', 'Green Bay Packers':'#203731', 'Houston Texans':'#03202f', 'Indianapolis Colts':'#002c5f', 'Jacksonville Jaguars':'#006778', 
                'Kansas City Chiefs':'#e31837', 'Los Angeles Chargers':'#002a5e', 'Los Angeles Rams':'#003594', 'Miami Dolphins':'#008e97', 
                'Minnesota Vikings':'#4f2683', 'New England Patriots':'#002244', 'New Orleans Saints':'#d3bc8d', 'New York Giants':'#0b2265', 
                'New York Jets':'#125740', 'Las Vegas Raiders':'#000000', 'Philadelphia Eagles':'#004c54', 'Pittsburgh Steelers':'#ffb612', 
                'San Francisco 49ers':'#aa0000', 'Seattle Seahawks':'#002244', 'Tampa Bay Buccaneers':'#d50a0a', 'Tennessee Titans':'#0c2340', 'Washington Football Team':'#773141'}

    rows = pd.read_csv('NFL_QB_Search.csv')
    player_img = pd.read_csv('NFL_QB_Search_Images.csv')
    qb_data = pd.DataFrame(rows)
    qb_img = pd.DataFrame(player_img)

    #qb_data.columns = ['Player','Image_Url','Image','Team','Age','GP','GS','Record','Wins %','Cmp','Att','Cmp%','Yds','TD','TD%','INT','INT%','1D','Lng','Y/A','AY/A','Y/C','Y/G','Rating','QBR','Sck','Sck%','Yds Loss']
    qb_data.columns = ['Player','Team','Age','GP','GS','Cmp','Att','Cmp%','Yds','TD','TD%','INT','INT%','Lng','Y/A','AY/A','Y/C','Y/G','Rating','Year']
    qb_img.columns = ['Player','Player Image','Year']

    current_season = 2021
    sorted_unique_players = sorted(qb_data.Player.unique())
    #years = range(1960, current_season)
    years = []


    # Selecting a Player
    user_input = st.selectbox('Select a player to search', sorted_unique_players)



    # Grab Active Years of Player in the NFL
    years_qb = qb_data.loc[qb_data['Player']== user_input, ['Year']]
    for i in years_qb['Year']:
        years.append(i)


    # Selecting a year based on user input (selected player)
    if user_input:
        selected_years = st.selectbox('Select a Year', list(reversed(years)))


    # Getting Team Color (if available) based on user input and selected year
    qb_team = qb_data.loc[qb_data['Player']== user_input, ['Team','Year']]
    qb_current_team = qb_team.loc[qb_team['Year']== selected_years, ['Team']]
    Team = ''
    year_check = 0
    if user_input and selected_years:
        for i in qb_current_team.Team:
            Team = i
        for j in qb_team.Year:
            if j == selected_years:
                year_check = j
        #st.write(Team, year_check)


    col1, col2= st.columns([1,1])

    if qb_img.Player.isin([user_input]).any():
    #if user_input:
        player_image = qb_img.loc[qb_img['Player']== user_input, ['Player Image']]
        for i in player_image['Player Image']:
            get_url = requests.get(i)
            img = Image.open(BytesIO(get_url.content))
            col1.image(img, width=250, caption=user_input)
            break

    # QB Placeholder Image if the player did not have an image collected during webscraping
    if not qb_img.Player.isin([user_input]).any():
        qb_img_placeholder = Image.open('qb_playerholder_img.jpg')
        col1.image(qb_img_placeholder, width=350, caption=user_input)    


    #   Naveen Venkatesan --> Data Scientist url:https://towardsdatascience.com/scraping-nfl-stats-to-compare-quarterback-efficiencies-4989642e02fe
    #   This is where I found a template for how to generate radar charts for comparing nfl quarterbacks
    # Stat Categories
    # Cmp%, Pass Yds, Passing TDs, TD%, INT, INT%, Rating

    #stat_categories = ['Completion Percentage','Passing Yards','Passing Touchdowns','Touchdown Percentage','Interceptions','Rating']

    # Reducing items in dataframe based on selected year
    stats_selected_year = qb_data[qb_data['Year'] ==selected_years]
    stats_selected_year_df = pd.DataFrame(stats_selected_year)

    # Checking that new df works 
    #st.dataframe(stats_selected_year_df)

    stat_categories = ['Cmp%','Yds','TD','TD%','INT%','Rating']
    #stats_data_categories_rankings = df['Cmp%','Pass Yds','Pass TD','TD%','INT','QBR']

    # Original
    #stats_data_categories = qb_data[['Player','Team'] + stat_categories] 

    # Demo
    stats_data_categories = stats_selected_year_df[['Player','Team'] + stat_categories] 


    # Convert data to numerical values (Original)
    #for i in stat_categories:
    #    stats_data_categories[i] = pd.to_numeric(qb_data[i])

    # Convert data to numerical values (Demo)
    for i in stat_categories:
        stats_data_categories[i] = pd.to_numeric(stats_selected_year_df[i])


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


    # Unique Player Create Figure
    fig_player = plt.figure(figsize=(8, 8), facecolor='white')# Add subplots
    ax2 = fig_player.add_subplot(222, projection='polar', facecolor='#ededed')
    data_demo_player = get_qb_player_data(stats_data_categories, user_input)# Plot QB data


    if user_input and selected_years:
        if Team not in team_colors:
            custom_color='blue'
            if st.sidebar.checkbox('Custom Color'):
                custom_color = st.sidebar.color_picker("Pick a custom color for player chart")
                #custom_color = st.sidebar.text_input("Enter a custom color for chart")
                st.sidebar.info('You can type in a color to customize the radar chart to your liking. Blue, Teal, Red perhaps? Just enter it to give it a try. Note: The default color is blue if text is left empty.')
            ax2 = create_radar_chart(ax2, angles, data_demo_player, color=custom_color)
        else:
            ax2 = create_radar_chart(ax2,angles,data_demo_player, team_colors[Team])
        col2.pyplot(fig_player)
        col2.write('As displayed above, the main points of emphasis that I have selected to compare for the quarterbacks in regards to the passing game are: Cmp%, Pass Yds, Passing TDs, TD%, INT, INT%, Rating. The greater the height and shape of one category, the better the player was in that category.')



        # DataFrame for Team Passing Rankings
        #Player_Ranks_df = stats_data_categories.loc[stats_data_categories['Player']==user_input]
        Player_Ranks_df = qb_data.loc[qb_data['Player']==user_input]
        Player_Ranks_df_selected_year = Player_Ranks_df.loc[Player_Ranks_df['Year']==selected_years]
        st.markdown(user_input + ' ' + str(selected_years) + ' Passing Stats')
        st.dataframe(Player_Ranks_df_selected_year)


        if st.sidebar.checkbox('Career'):
            st.subheader(user_input + ' Career Passing Stats')
            st.dataframe(Player_Ranks_df)



        # **************** Ranking(s) **************************************
        # ['Cmp%','Yds','TD','TD%','INT','Rating']

    if selected_years >= 1960 and selected_years < 1970:
        rankings_df = stats_data_categories.head(20)
    else:
        rankings_df = stats_data_categories.head(32)

    if st.sidebar.checkbox('Passing Stats ' + str(selected_years) + ' Season'):
        st.caption('A DataFrame of the Quarterbacks in regards to Passing Yards (Depicted Below)')
        st.dataframe(rankings_df)

    for i in rankings_df:
        if i == 'Cmp% Rank':
            cmp_perc_type = rankings_df[i].astype(float)
            cmp_rank_value = cmp_perc_type * 10
            #st.write(cmp_rank_value)
        if i == 'Yds Rank':
            pass_yds_type = rankings_df[i].astype(float)
            pass_yds_rank_value = pass_yds_type * 10
            #st.write(pass_yds_rank_value)
        if i == 'TD Rank':
            pass_td_type = rankings_df[i].astype(float)
            pass_td_value = pass_td_type * 10
            #st.write(pass_td_value)
        if i == 'TD% Rank':
            td_perc_type = rankings_df[i].astype(float)
            td_perc_rank_value = td_perc_type * 10
            #st.write(td_perc_rank_value)
        if i == 'INT% Rank':
            int_perc_type = rankings_df[i].astype(float)
            int_perc_rank_value = int_perc_type * 10
            #st.write(int_perc_rank_value)
        if i == 'Rating Rank':
            rating_type = rankings_df[i].astype(float)
            rating_rank_value = rating_type * 50
            #st.write(QBR_rank_value)
        
    rankings_df['Player Rating'] = cmp_rank_value + pass_yds_rank_value + pass_td_value + td_perc_rank_value + int_perc_rank_value + rating_rank_value
    player_ratings = rankings_df[[ 'Player','Player Rating']]
    player_ratings = player_ratings.sort_values(by=['Player Rating'], ascending=False)


    # Display ratings in descending order for players under the passing stats category
    #st.caption('A DataFrame of the Top 32 Quarterbacks sorted by Player Rating, which was calculated based on the QBRanking Formula.')
    #st.dataframe(player_ratings)

    if st.sidebar.checkbox('Rankings'):

        if selected_years >= 1960 and selected_years < 1970:
            col11, col22 = st.columns(2)
            # Top 10 Quarterbacks 
            col11.subheader('Top 10 Rated Quarterbacks')
            top = player_ratings.head(10)
            col11.dataframe(top)

            # Bottom 10 Quarterbacks 
            col22.subheader('Bottom 10 Rated Quarterbacks')
            bottom = player_ratings.tail(10)
            col22.dataframe(bottom)

        else:
            # Making the dataframe(s) based on top, middle, bottom classifications prettier
            col11, col22, col33 = st.columns(3)

            # Top 10 Quarterbacks 
            col11.subheader('Top 10 Rated Quarterbacks')
            top = player_ratings.head(10)
            col11.dataframe(top)
            #st.dataframe(player_ratings.head(10))

            # Average (Middle of The Pack) Quarterbacks
            col22.subheader('"Middle Of The Pack" Rated Quarterbacks')
            middle = player_ratings[10:22]
            col22.dataframe(middle)
            #st.dataframe(player_ratings[10:22])   

            # Bottom 10 Quarterbacks 
            col33.subheader('Bottom 10 Rated Quarterbacks')
            bottom = player_ratings.tail(10)
            col33.dataframe(bottom)
            #st.dataframe(player_ratings.tail(10))

    # length of dataframe ranking
    ranking_len = len(player_ratings)

    # Checking ranking_len
    #st.write(ranking_len)

    # list of players
    players_sorted_ratings = list()

    # Checking Player Rank ( #N out of ranking_len)
    for i in player_ratings.Player:
        players_sorted_ratings.append(i)

    #st.write(players_sorted_ratings)

    for i in players_sorted_ratings:
        if i == user_input:
            player_index = players_sorted_ratings.index(i)
        if user_input not in players_sorted_ratings:
            player_index = -1
    player_rank = player_index + 1
    #st.write(player_rank)


    if user_input and player_index >= 0:
        col1.success(user_input + ' ranked ' + str(player_rank) + ' out of ' + str(ranking_len) + ' quaterbacks during the ' + str(selected_years) + ' season.')
    if user_input and  player_index == -1: 
        col1.error('Not enough data to be ranked for the ' + str(selected_years) + ' season.')
