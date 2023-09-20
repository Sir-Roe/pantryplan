from bs4 import BeautifulSoup
from pathlib import Path
import itertools
import pandas as pd
import requests
import os




tbl_dir = os.path.join(Path(__file__).parents[0], 'recipe_scraper_tables')



def grab_cat_urls():
    
    all_url = "https://www.allrecipes.com/recipes-a-z-6735880"

    response=requests.get(all_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.body.main

        #WHERE all recipe data is stored
    else:
        print("Failed to retrieve the web page.")

    #------------------------------------------------------------
    #----------Create DF of all URLs to each category------------
    #------------------------------------------------------------
    a_elements = body.find_all('a', class_='link-list__link type--dog-bold type--dog-link')
    href=[]
    text =[]

    # Iterate through the found <a> elements and print their text and href attributes
    for a in a_elements:
        href.append(a.get('href'))
        text.append(a.text.strip())

    df_ref = pd.DataFrame({'URL': href, 'Category': text})
    df_ref['Category']=df_ref['Category'].str.replace(' ','_').str.lower()
    df_ref.to_csv(f'{tbl_dir}\category_urls.csv',index=False)
    return df_ref

def grab_cat_urls(df=''):
    if len(df)==0:
        df = pd.read_csv(f'{tbl_dir}\category_urls.csv')

    df = df.reset_index()  # make sure indexes pair with number of rows

    for index, row in df.iterrows():
        recipe_url_scrape(row['URL'], row['Category'])

    return print("Complete url list Generated!")


def recipe_url_scrape(url,cat=''):

    response=requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        #WHERE all recipe data is stored
        body = soup.body.main
    else:
        print("Failed to retrieve the web page.")

    a_elements = body.find_all('a', class_='comp card--image-top mntl-card-list-items mntl-document-card mntl-card card card--no-image')
    href=[]
    rec_id=[]
    # Iterate through the found <a> elements and print their text and href attributes
    for a in a_elements:
        href.append(a.get('href'))
        rec_id.append(a.get('data-doc-id'))

    #-----------------------
    #--grab header recipes--
    #-----------------------

    a_elements = body.find_all('a', class_='comp mntl-card-list-items mntl-document-card mntl-card card card--no-image')

    # Iterate through the found <a> elements and print their text and href attributes
    for a in a_elements:
        href.append(a.get('href'))
        rec_id.append(a.get('data-doc-id'))

    #build df    
    cat_df= pd.DataFrame({'category':cat,'id_recipe':rec_id,'url_recipe': href})

    cat_df.to_csv(f'{tbl_dir}\{cat}_urls.csv',index=False)

    return cat_df

grab_cat_urls()