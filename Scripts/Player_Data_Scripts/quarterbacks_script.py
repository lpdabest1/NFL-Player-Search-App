from ast import Index
from pandas.core.base import SelectionMixin
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# calculating current nfl season as most recent season available to scrape
current_season = 2021
selected_year = range(1960, current_season)
players = []
player_images = []

def scraping_qb_stats(selected_year):
    for i in selected_year:
        url = 'https://www.pro-football-reference.com/years/'+ str(i) + '/passing.htm'
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
                        
                        ranking_search = i.find('th', {'data-stat':'ranker'})
                        ranking = ranking_search['csk']

                        
                        names_search = i.find('td', {'data-stat':'player'})
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

                        
                        passes_completed_search = i.find('td',{'data-stat':'pass_cmp'})
                        passes_completed = passes_completed_search.text        

                        
                        passes_attempted_search = i.find('td',{'data-stat':'pass_att'})
                        passes_attempted = passes_attempted_search.text       


                        
                        completion_percentage_search = i.find('td',{'data-stat':'pass_cmp_perc'})
                        completion_percentage = completion_percentage_search.text         


                        
                        passing_yards_search = i.find('td',{'data-stat':'pass_yds'})
                        passing_yards = passing_yards_search.text         


                        
                        passing_touchdowns_search = i.find('td',{'data-stat':'pass_td'})
                        passing_touchdowns = passing_touchdowns_search.text
                    

                        
                        touchdown_percentage_search = i.find('td',{'data-stat':'pass_td_perc'})
                        touchdown_percentage = touchdown_percentage_search.text

                      
                        interceptions_search = i.find('td',{'data-stat':'pass_int'})
                        interceptions = interceptions_search.text


                        
                        interception_percentage_search = i.find('td',{'data-stat':'pass_int_perc'})
                        interception_percentage = interception_percentage_search.text


                        
                        pass_long_search = i.find('td',{'data-stat':'pass_long'})
                        pass_long = pass_long_search.text


                       
                        yards_per_attempt_search = i.find('td',{'data-stat':'pass_yds_per_att'})
                        yards_per_attempt = yards_per_attempt_search.text


                        
                        adj_yards_per_attempt_search = i.find('td',{'data-stat':'pass_adj_yds_per_att'})
                        adj_yards_per_attempt = adj_yards_per_attempt_search.text


                        
                        yards_per_completion_search = i.find('td',{'data-stat':'pass_yds_per_cmp'})
                        yards_per_completion = yards_per_completion_search.text


                        
                        yards_per_game_search = i.find('td',{'data-stat':'pass_yds_per_g'})
                        yards_per_game = yards_per_game_search.text


                        
                        passer_rating_search = i.find('td',{'data-stat':'pass_rating'})
                        passer_rating = passer_rating_search.text


                        #Formatting Data Collected
                        player = { "Player": names, "Team": team, "Age": age, "Games Played": games, "Games Started": games_played, 
                    "Passes Completed": passes_completed, "Passes Attempted": passes_attempted, "Completion Percentage": completion_percentage, "Passing Yards": passing_yards, "Passing Touchdowns": passing_touchdowns,
                    "Touchdown Percentage": touchdown_percentage, "Interceptions": interceptions, "Interceptions Percentage": interception_percentage, "Longest Pass": pass_long,
                    "Yards Per Attempt": yards_per_attempt, "Adjusted Yards Per Attempt": adj_yards_per_attempt, "Yards per Completion": yards_per_completion, "Yards Per Game": yards_per_game,
                    "Passer Rating": passer_rating, "Year": year}
                        #Appending Each player to Players List
                        players.append(player)
            
            
                #print(ranking, names, team, age, games, games_played)
            
                        break
                    except:
                        break




    df = pd.DataFrame(players)
    df.to_csv("NFL_QB_Search.csv", index=False)
    #print(df)
    return df
df = scraping_qb_stats(selected_year)

#########################################################################################
# Player Image Scraper Starts Here

def load_data(selected_year):
    for i in selected_year:
        url = 'https://www.pro-football-reference.com/years/' + str(i) + '/passing.htm'
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
                        names_text = names_search.find('a')
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
 
                                        player_images.append(player_image)
                                        
                                    else:
                                        break
                                except:
                                    break
                        break
                    except:
                        break

            
    df2 = pd.DataFrame(player_images)
    df2.to_csv("NFL_QB_Search_Images.csv", index=False)
    return df2
df2 = load_data(selected_year)
