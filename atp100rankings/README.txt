ATP 100 Rankings Web Scraping

Overview:
---------
This Python script is designed to scrape the ATP (Association of Tennis Professionals) website for the ATP 100 rankings. The script retrieves the rankings for each week and stores the data in a pandas DataFrame. Additionally, it outputs the data to a CSV file named 'atp100rankingsbyweek.csv'.

Requirements:
-------------
- Python 3.x
- Required Python libraries: requests, bs4 (Beautiful Soup), pandas
Usage:
------
1. Ensure you have all the required Python libraries installed. You can install them using pip:
   
pip install requests
pip install beautifulsoup4
pip install pandas


2. Place the provided Python script ('atp_rankings_scraper.py') in your working directory.

3. Execute the script using a Python interpreter:

python atp_rankings_scraper.py


4. The script will fetch the ATP 100 rankings for the specified number of weeks (default is 10 weeks). The data will be displayed on the console, and it will be stored in a CSV file named 'atp100rankingsbyweek.csv'.

5. You can modify the number of weeks to fetch by changing the value of the 'amt_weeks' variable inside the script.

Output:
-------
The script outputs the ATP 100 rankings data in tabular format. Each row represents a player's ranking for a specific week, including their country, player name, and points. The data is also saved to a CSV file for further analysis or storage.

Disclaimer:
-----------
This script relies on web scraping techniques to extract data from the ATP website. Please use responsibly and be respectful of the website's terms of service and usage policies. The script may need adjustments if the structure of the ATP website changes.
