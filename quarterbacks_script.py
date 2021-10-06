
from pandas.core.base import SelectionMixin
import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import random
import re
import urllib.request
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpim
import numpy as np
from mpl_toolkits import mplot3d
import streamlit as st
import matplotlib.image as mpimg

from io import BytesIO
import urllib.request
#%matplotlib inline

def app():

    # calculating current nfl season as most recent season available to scrape
    current_rating_season = 2021
    #selected_year_input = input("Enter a year: ")
    #selected_year = (list(reversed(range(1932,last_passer_rating_season))))

    #selected_years = [str(i) for i in range(1932, 2006)]
    selected_years = 2021
    def scraping_QB_Stats(selected_years):
        players = []


        url = 'https://www.pro-football-reference.com/years/'+ str(selected_years) + '/passing.htm'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        page = requests.get(url,headers=headers, timeout=2, allow_redirects = True )
        soup = bs(page.content, 'html.parser')
        href_tbody = soup.find_all('tbody')

        for i in href_tbody:
            href_tr_data = i.find_all('tr')
            for i in href_tr_data:
                while True:
                    try:

                        '''Name of Player Collected'''
                        names_search = i.find('td', {'data-stat':'player'})
                        #names = names_search['csk']
                        names_text = names_search.find('a')
                        names = names_text.text


                        '''Team of PLayer Collected'''
                        team_search = i.find('td', {'data-stat':'team'})
                        team_name = team_search.find('a')
                        team = team_name['title']

                        '''Age of Player Collected '''
                        age_search = i.find('td',{'data-stat':'age'})
                        age = age_search.text

                        '''Games and Games played by Player Collected'''
                        games_search = i.find('td',{'data-stat':'g'})
                        games = games_search.text

                        games_played_search = i.find('td',{'data-stat':'gs'})
                        games_played = games_played_search.text
    
                        '''Passes Completed of Player Collected'''
                        passes_completed_search = i.find('td',{'data-stat':'pass_cmp'})
                        passes_completed = passes_completed_search.text        
    
                        '''Passes Attempted of Player Collected'''
                        passes_attempted_search = i.find('td',{'data-stat':'pass_att'})
                        passes_attempted = passes_attempted_search.text       


                        '''Completion Percentage of Player Collected'''
                        completion_percentage_search = i.find('td',{'data-stat':'pass_cmp_perc'})
                        completion_percentage = completion_percentage_search.text         


                        '''Passing Yards of Player Collected'''
                        passing_yards_search = i.find('td',{'data-stat':'pass_yds'})
                        passing_yards = passing_yards_search.text         


                        '''Passing Touchdowns of Player Collected'''
                        passing_touchdowns_search = i.find('td',{'data-stat':'pass_td'})
                        passing_touchdowns = passing_touchdowns_search.text
                    

                        '''Touchdown Percentage of Player Collected'''
                        touchdown_percentage_search = i.find('td',{'data-stat':'pass_td_perc'})
                        touchdown_percentage = touchdown_percentage_search.text

                        '''Interceptions of Player Collected'''
                        interceptions_search = i.find('td',{'data-stat':'pass_int'})
                        interceptions = interceptions_search.text


                        '''Interception Percentage of Player Collected'''
                        interception_percentage_search = i.find('td',{'data-stat':'pass_int_perc'})
                        interception_percentage = interception_percentage_search.text


                        '''Yards per Attempt of Player Collected'''
                        yards_per_attempt_search = i.find('td',{'data-stat':'pass_yds_per_att'})
                        yards_per_attempt = yards_per_attempt_search.text


                        '''Adjusted Yards per Attempt of Players Collected'''
                        adj_yards_per_attempt_search = i.find('td',{'data-stat':'pass_adj_yds_per_att'})
                        adj_yards_per_attempt = adj_yards_per_attempt_search.text


                        '''Yards per Completion of Players Collected'''
                        yards_per_completion_search = i.find('td',{'data-stat':'pass_yds_per_cmp'})
                        yards_per_completion = yards_per_completion_search.text


                        '''Yards per Game'''
                        yards_per_game_search = i.find('td',{'data-stat':'pass_yds_per_g'})
                        yards_per_game = yards_per_game_search.text


                        '''Rating'''
                        passer_rating_search = i.find('td',{'data-stat':'pass_rating'})
                        passer_rating = passer_rating_search.text

                        #Formatting Data Collected
                        player = { "Player": names, "Team": team, "Age": age, "Games Played": games, "Games Started": games_played,
                    "Passes Completed": passes_completed, "Passes Attempted": passes_attempted, "Completion Percentage": completion_percentage, "Passing Yards": passing_yards, "Passing Touchdowns": passing_touchdowns,
                    "Touchdown Percentage": touchdown_percentage, "Interceptions": interceptions, "Interceptions Percentage": interception_percentage,
                    "Yards Per Attempt": yards_per_attempt, "Adjusted Yards Per Attempt": adj_yards_per_attempt, "Yards per Completion": yards_per_completion, "Yards Per Game": yards_per_game,
                    "Passer Rating": passer_rating}
                        #Appending Each player to Players List
                        players.append(player)
            
            
                #print(ranking, names, team, age, games, games_played)
            
                        break
                    except:
                        break




        df = pd.DataFrame(players)
        return df
    df = scraping_QB_Stats(selected_years)



    def load_data(selected_years):
        player_images = []

        url = 'https://www.pro-football-reference.com/years/' + str(selected_years) + '/passing.htm'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        page = requests.get(url,headers=headers, timeout=2, allow_redirects = True )
        soup = bs(page.content, 'html.parser')
        href_tbody = soup.find_all('tbody')

        for i in href_tbody:
            href_tr_data = i.find_all('tr')
            for i in href_tr_data:
                while True:
                    try:
                        names_search = i.find('td', {'data-stat':'player'})
                    #names = names_search['csk']
                        names_text = names_search.find('a')
                        names = names_text.text
                        for link in names_search.find_all('a', href=True):
                            player_link = link['href']
                            base = 'https://www.pro-football-reference.com'
                            url = base + str(player_link)
                            page = requests.get(url,headers=headers, timeout=2, allow_redirects = True )
                            soup = bs(page.content, 'html.parser')
                            player_img = soup.find('div', {'class': 'media-item'})
                            img = player_img.find('img')
                            img_src = img['src']
                            #print(img_src) 


                            player_image = {
                                        "Player": names,
                                        "Player_Image": img_src
                                    }
                            player_images.append(player_image)

                        break
                    except:
                        break

        df3 = pd.DataFrame(player_images)
        return df3
    df3 = load_data(selected_years)
        # Player Image Scraper Ends Here

        # Merging the Statistics Dataframe with the Image DataFrame
    images_src = df3["Player_Image"]
    df_merged = df.join(images_src)
    df_merged = df_merged.astype({
                                'Player':'str',
                                'Team':'str',
                                'Age':'int',
                                'Passes Completed':'int',
                                'Passes Attempted':'int',
                                'Completion Percentage':'str',
                                'Passing Yards':'int',
                                'Passing Touchdowns':'int',
                                'Touchdown Percentage':'str',
                                'Interceptions':'int',
                                'Interceptions Percentage':'str',
                                'Yards Per Attempt':'str',
                                'Adjusted Yards Per Attempt':'str',
                                'Yards per Completion':'str',
                                'Yards Per Game':'str',
                                'Passer Rating':'str',                                   
                                })

    #print(df_merged)
    df.to_csv('quarterbacks_stats',index=False)

