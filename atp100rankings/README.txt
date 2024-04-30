**ATP 100 Rankings Web Scraping**

Overview:
---------

This Python script is designed to scrape the ATP (Association of Tennis Professionals) website for the ATP 100 rankings. The script retrieves the rankings for each week and stores the data in a pandas DataFrame. Additionally, it outputs the data to a CSV file named 'atp100rankingsbyweek.csv' and a PDF file named 'atp100_analytics.pdf'.

Requirements:
-------------

- Python 3.x
- Required Python libraries: inserted to the file requirements.txt

Usage:
------

1. Place the provided Python script ('atp_rankings_scraper.py') and the .txt file ('requirements.txt') in your working directory.

2. Execute the script using a Python interpreter:

   python atp_rankings_scraper.py

3. The script will fetch the ATP 100 rankings for the specified number of weeks (default is number of weeks for year 2024). The data will be displayed on the console, and it will be stored in a CSV file named 'atp100rankingsbyweek.csv' and will be generated a PDF file named 'atp100_analytics.pdf'.

4. You can modify the number of weeks to fetch by changing the value of the 'amt_weeks' variable inside the script.

Output:
-------

The script outputs the ATP 100 rankings data in tabular format. Each row represents a player's ranking for a specific week, including their country, player name, points earned/dropped in the current week (+/-), and the total tournaments played. The data is also saved to a CSV file for further analysis or storage.

Disclaimer:
-----------

This script relies on web scraping techniques to extract data from the ATP website. Please use responsibly and be respectful of the website's terms of service and usage policies. The script may need adjustments if the structure of the ATP website changes.
