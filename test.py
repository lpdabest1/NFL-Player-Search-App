from ast import Index
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
#%matplotlib inline



# calculating current nfl season as most recent season available to scrape
current_season = 2021
#selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,current_season))))
selected_year = range(1960, current_season)
player_images = []


def load_data(selected_year):
    for i in selected_year:
        url = 'https://www.pro-football-reference.com/years/' + str(i) + '/passing.htm'
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'}
        page = requests.get(url,headers=headers, timeout=2, allow_redirects = True )
        soup = bs(page.content, 'html.parser')
        href = soup.find('table', {'id': 'passing'})
        href_th = soup.find_all('th',{'class':'right'})
        href_tbody = soup.find_all('tbody')
        href_tr = soup.find_all('tr')
        year = i

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

                            if soup.find('div', {'class': 'media-item'}):
                                player_img = soup.find('div', {'class': 'media-item'})


                                img = player_img.find('img')
                                img_src = img['src'] 
                                print(img_src, year)
                                # Player Name
                                player_name = soup.find('h1', {'itemprop': 'name'})
                                player_name_span = player_name.find('span')
                                player_name_text = player_name_span.text
                                    
                                player_image = {
                                    "Player": player_name_text,
                                    "Player Image": img_src,
                                    "Year": year
                                                }
                                player_images.append(player_image)

                        break
                    except:
                        break

            
    df2 = pd.DataFrame(player_images)
    df2.to_csv("NFL_QB_Search_Images_Test.csv", index=False)
    return df2
df2 = load_data(selected_year)