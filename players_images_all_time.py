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
import matplotlib.image as mpimg

from io import BytesIO
import urllib.request

players_image_urls = []

url = 'https://www.pro-football-reference.com/players/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}
page = requests.get(url,headers=headers, timeout=2, allow_redirects = True )
soup = bs(page.content, 'html.parser')
#ref_alphabet = soup.find('ul',{'class':'alphabet bullets-inline'})
ref_alphabet = soup.find('ul',{'class':'page_index'})
#Iterate through the alphabet to get each player according to the first letter of their last name (all players who have ever been recorded by pro football reference)
# We will be using a for loop to carryout the iteration(s)                    
#for i in ref_alphabet:                        
#ref_li = i.find_all('li')
#for li in ref_alphabet.find_all('li'):
#    print(li.text, end="")

ref_li = ref_alphabet.find_all('li')
for j in ref_li:
    while True:
        try:
                
            ref_li_letter = j.find('a', href=True)
            #print(ref_li_letter)
            for a_href in j.find_all('a', href=True): #ref_li_letter.find_all('a', href=True):
                alphabet_letter_ref = a_href['href']
                base = 'https://www.pro-football-reference.com'
                url = base + str(alphabet_letter_ref)

                #print(url)

                page = requests.get(url,headers=headers, timeout=2, allow_redirects = True )
                soup = bs(page.content, 'html.parser')
                players_section = soup.find('div',{'id':'div_players'})

                #print(players_section)

                for a_href_players in players_section.find_all('a', href=True):

                    player_link = a_href_players['href']


                    #print(player_link)

                    base = 'https://www.pro-football-reference.com'
                    url = base + str(player_link)
                    page = requests.get(url,headers=headers, timeout=2, allow_redirects = True )
                    soup = bs(page.content, 'html.parser')
                        
                    # Player Image

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
                                "Player_img": img_src
                                            }
                            players_image_urls.append(player_image)

                            if not soup.find('div', {'class': 'media-item'}):
                                break
                                
                        except:
                            break


            break
        except:
            break

print('process done')
player_img_df = pd.DataFrame(players_image_urls)
print(player_img_df.head)

player_img_df.to_csv('players_img_edited.csv', index=False)
