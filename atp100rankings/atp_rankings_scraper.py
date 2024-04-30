import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

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
        content_age_player_list = soup.find_all('td', class_ = 'age small-cell')[:100]
        age_player_list = list(map(lambda x: x.text.strip('\n'),content_age_player_list))
        
        #Find the ages of players list
        content_player_list = soup.find_all('li', class_ = 'name center')[:100]
        player_list = list(map(lambda x: x.text.strip('\n'),content_player_list))

        #Find total points list
        content_player_points_list = soup.find_all('td', class_ = 'points center bold extrabold small-cell')[:100]
        player_points_list = list(map(lambda x: x.text.strip(' \r\n '),content_player_points_list))
        
        #Difference of points earned/dropped in current week (+/-)
        content_difference_points_list = soup.find_all('td', class_ = re.compile(r'^small-cell pointsMove center'))[:100]
        player_diff_points_list = list(map(lambda x: x.text.strip(' \r\n ') ,content_difference_points_list))
        

        
        #Tournaments played for each player
        content_tourn_played_list = soup.find_all('td', class_ = 'tourns center small-cell')[:100]
        player_tourn_played_list = list(map(lambda x: x.text.strip(' \r\n '),content_tourn_played_list))
        
        dict_temp = {'week': [week]* 100, 
                     'ranking':ranking_list, 
                     'country': country_list, 
                     'player': player_list, 
                     'age': age_player_list, 
                     'points': player_points_list,
                     '(+/-)': player_diff_points_list,
                     'tournaments_played':player_tourn_played_list}
        
        df_dict_temp = pd.DataFrame(dict_temp)
        
        try:
            df =  pd.concat([df, df_dict_temp], ignore_index=True)
        except:
            df = pd.DataFrame(dict_temp)
        
         
        # Filter the week_list to include only weeks for 2024.You can change the year by changing the inserted value of week.startswith('2024')
        if  amt_weeks == 1:   
            weeks_2024 = [week for week in week_list if week.startswith('2024')] 
        #Change amt_weeks regarding the amount of weeks you want  
        if amt_weeks == len(weeks_2024):
            print(amt_weeks)
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


# Replace '-' with '0' using regex
df['(+/-)'] = df['(+/-)'].replace(r'^-$', '0', regex=True)

# Preprocess data to calculate total points earned/lost for each player from the same country in each week
df['(+/-)'] = df['(+/-)'].astype(int)
df_grouped = df.groupby(['week', 'country'])['(+/-)'].sum().reset_index()

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_filename = os.path.join(current_dir, 'atp100_analytics.pdf')

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_filename = os.path.join(current_dir, 'atp100_analytics.pdf')
csv_filename = os.path.join(current_dir, 'atp100rankingsbyweek.csv')

# Save the plots to a PDF file
with PdfPages(pdf_filename) as pdf:
    # Plotting for each week
    for week in df['week'].unique():
        # Combined plot to show which country has earned or lost points as a total of its players
        plt.figure(figsize=(18, 10))
        df_grouped_sorted = df_grouped.sort_values(by='(+/-)', ascending=False)
        sns.barplot(data=df_grouped_sorted[df_grouped_sorted['week'] == week], x='(+/-)', y='country', hue='country', dodge=False, palette='viridis', legend=False)
        plt.title(f'Points Lost or Earned by Players from the same Country - Week {week}')
        plt.xlabel('Total Points Lost or Earned')
        plt.ylabel('Country')
        plt.tight_layout()
        # Save the current figure to a page in the PDF file
        pdf.savefig()  
        plt.close()
        #We want an example of the current week so we add a break.Comment break command if you want a figure for each week
        break
    
    # Plotting for the year 2024
    plt.figure(figsize=(18, 10))
    df_grouped = df.groupby(['country'])['(+/-)'].sum().reset_index()
    df_grouped_sorted = df_grouped.sort_values(by='(+/-)', ascending=False)
    sns.barplot(data=df_grouped_sorted, x='(+/-)', y='country', palette='viridis')
    plt.title('Points Lost or Earned by Players from the same Country - 2024')
    plt.xlabel('Total Points Lost or Earned')
    plt.ylabel('Country')
    plt.tight_layout()
    # Save the current figure to a page in the PDF file
    pdf.savefig()  
    plt.close()

print(f"PDF '{pdf_filename}' generated successfully.")

# Output the df to a csv file for further analysis
df.to_csv(csv_filename)

print(f"CSV '{csv_filename}' generated successfully.")

