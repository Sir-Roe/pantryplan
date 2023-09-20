from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import requests
import os


stp_dir = os.path.join(Path(__file__).parents[0], 'recipe_scraper_table')


response=requests.get(all_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    #WHERE all recipe data is stored
else:
    print("Failed to retrieve the web page.")