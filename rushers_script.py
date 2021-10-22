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

# calculating current nfl season as most recent season available to scrape
current_season = 2021
#selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,current_season))))
selected_year = range(1960, current_season)
players = []
player_images = []



def scraping_rb_stats(selected_year):
    for i in selected_year:
    
        


        url = 'https://www.pro-football-reference.com/years/'+ str(i) + '/rushing.htm'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        page = requests.get(url,headers=headers, timeout=5, allow_redirects = True )
        soup = bs(page.content, 'html.parser')
        href_tbody = soup.find_all('tbody')

        year = str(i)





        for i in href_tbody:
            href_tr_data = i.find_all('tr')
            for i in href_tr_data:
                while True:
                    try:
                        
                        names_search = i.find('td', {'data-stat':'player'})
                        #names = names_search['csk']
                        names_text = names_search.find('a')
                        names = names_text.text


                        
                        team_search = i.find('td', {'data-stat':'team'})
                        team_name = team_search.find('a')
                        team = team_name['title']

                        
                        age_search = i.find('td',{'data-stat':'age'})
                        age = age_search.text

                        
                        games_search = i.find('td',{'data-stat':'g'})
                        games = games_search.text

                        games_played_search = i.find('td',{'data-stat':'gs'})
                        games_played = games_played_search.text     

                        
                        rush_att_search = i.find('td',{'data-stat':'rush_att'})
                        rush_att = rush_att_search.text        

                        
                        rush_yds_search = i.find('td',{'data-stat':'rush_yds'})
                        rush_yds = rush_yds_search.text       


                        
                        rush_td_search = i.find('td',{'data-stat':'rush_td'})
                        rush_td = rush_td_search.text         


                        
                        rush_long_search = i.find('td',{'data-stat':'rush_long'})
                        rush_long = rush_long_search.text         


                        
                        rush_yds_per_att_search = i.find('td',{'data-stat':'rush_yds_per_att'})
                        yds_per_att = rush_yds_per_att_search.text
                    

                        
                        rush_yds_per_g_search = i.find('td',{'data-stat':'rush_yds_per_g'})
                        yds_per_g = rush_yds_per_g_search.text

                      
                        fumbles_search = i.find('td',{'data-stat':'fumbles'})
                        fumbles = fumbles_search.text

                        #Formatting Data Collected
                        player = { "Player": names, "Team": team, "Age": age, "Games Played": games, "Games Started": games_played, 
                                   "Att": rush_att, "Yards": rush_yds, "TD": rush_td, "Long": rush_long,
                                   "Y/A": yds_per_att, "Y/G": yds_per_g, "Fumbles": fumbles, "Year": year}
                        #Appending Each player to Players List
                        players.append(player)
            
            
                #print(ranking, names, team, age, games, games_played)
            
                        break
                    except:
                        break




    df = pd.DataFrame(players)
    df.to_csv("NFL_RB_Search.csv", index=False)
    #print(df)
    return df
df = scraping_rb_stats(selected_year)

    #########################################################################################
    # Player Image Scraper Starts Here

    #def load_data(i):
    #player_images = []

def load_data(selected_year):
    for i in selected_year:
        url = 'https://www.pro-football-reference.com/years/' + str(i) + '/rushing.htm'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        page = requests.get(url,headers=headers, timeout=2, allow_redirects = True )
        soup = bs(page.content, 'html.parser')
        href = soup.find('table', {'id': 'rushing'})
        href_th = soup.find_all('th',{'class':'right'})
        href_tbody = soup.find_all('tbody')
        href_tr = soup.find_all('tr')


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

                            while True:
                                try:
                                    if soup.find('div', {'class': 'media-item'}):
                                        player_img = soup.find('div', {'class': 'media-item'})


                                        img = player_img.find('img')
                                        img_src = img['src'] 
                                        
                                        # Player Name
                                        player_name = soup.find('h1', {'itemprop': 'name'})
                                        player_name_span = player_name.find('span')
                                        player_name_text = player_name_span.text
                                            
                                        player_image = {
                                            "Player": player_name_text,
                                            "Player Image": img_src,
                                            
                                                        }

                                        #Check code output
                                        player_images.append(player_image)
                                        break
                                        #print(player_images)
                                    else:
                                        break
                                except:
                                    break
                        break
                    except:
                        break

            
    df2 = pd.DataFrame(player_images)
    df2.to_csv("NFL_RB_Search_Images.csv", index=False)
    return df2
df2 = load_data(selected_year)

#images_src = df2["Player Image"]
#df_merged = df.join(images_src)


#df = pd.DataFrame(players)
#print(df)

