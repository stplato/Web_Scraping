import requests
from bs4 import BeautifulSoup
import pandas as pd



def get_atp_100_info(week_list):
    BASE_URL = "https://www.atptour.com/en/rankings/singles?RankRange=0-100&Region=all&DateWeek"
    extra_url = '&SortField=Ranking&SortAscending=True'
    amt_weeks = 0
    df = pd.DataFrame()
    for week in week_list:
        amt_weeks +=1
        #Find each url
        url = BASE_URL + '=' + week + extra_url
        
        #Go inside url to get info
        response = requests.get(url)
        headers = {"user-Agent": "Chrome"}
        response = requests.get(url, headers=headers)
        #print(response.status_code)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        #Find the ranking
        content_ranking_list = soup.find_all('td', class_ = 'rank bold heavy tiny-cell')[:100]
        ranking_list = list(map(lambda x: x.text.strip('\n'),content_ranking_list))
       

        #Find the country list
        content_country_list = soup.find_all('img', class_ = 'flag')[:100]
        country_list = list(map(lambda x: x.get('src').split('/')[-1].split('.')[-2],content_country_list))
        

        #Find the player list
        content_player_list = soup.find_all('li', class_ = 'name center')[:100]
        player_list = list(map(lambda x: x.text.strip('\n'),content_player_list))
        

        #Find total points list
        content_player_points_list = soup.find_all('td', class_ = 'points center bold extrabold small-cell')[:100]
        player_points_list = list(map(lambda x: x.text.strip(' \r\n '),content_player_points_list))
        

        dict_temp = {'week': [week]* 100, 'ranking':ranking_list, 'country': country_list, 'player': player_list, 'points': player_points_list}
        
        df_dict_temp = pd.DataFrame(dict_temp)
        
        try:
            df =  pd.concat([df, df_dict_temp], ignore_index=True)
        except:
            df = pd.DataFrame(dict_temp)
        
        #Change amt_weeks regarding the amount of weeks you want    
        if amt_weeks == 10:
            break
        
    return df

BASE_URL = "https://www.atptour.com/en/rankings/singles?RankRange=0-100&Region=all&DateWeek"

#Go inside url to get info
response = requests.get(BASE_URL)
headers = {"user-Agent": "Chrome"}
response = requests.get(BASE_URL, headers=headers)
#print(response.status_code)
soup = BeautifulSoup(response.content, 'html.parser')

#Find the week list
content_date_list = soup.find_all('div', class_ ='dropdown')[-1].text.strip('\n')
week_list = content_date_list.replace('.','-').split('\n')

df = get_atp_100_info(week_list)

print(df)

# Output the df to a csv file
df.to_csv('atp100rankingsbyweek.csv', index=False)