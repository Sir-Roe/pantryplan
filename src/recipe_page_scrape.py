from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd
import requests
import os


rec_dir = os.path.join(Path(__file__).parents[0], 'recipe_data')
ing_dir = os.path.join(Path(__file__).parents[0], 'ingredients_data')
stp_dir = os.path.join(Path(__file__).parents[0], 'steps_data')

def scrape_recipe(url=''):
    '''
    This function scrapes the relevant info
    from each individual recipe. It grabs ingredients
    for a seperate table. There is a main DF for recipe
    header info and an Ingredients DF to track ingredients
    '''
    url = "https://www.allrecipes.com/air-fryer-hearts-of-palm-sticks-recipe-7814346"

    response=requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        #WHERE all recipe data is stored
        soup = soup.body.main.article
    else:
        return print("Failed to retrieve the web page.")

    #scrape the unique key for the recipe
    start=url.rfind('-')+1
    rkey=url[start:]
    #build recipe dictionary
    recipe ={}
    recipe['id_recipe']=rkey
    #grab the header prep time info
    rlabels = soup.find_all("div", {"class": "mntl-recipe-details__label"})
    rinfo = soup.find_all("div", {"class": "mntl-recipe-details__value"})

    label=[lab.text for lab in rlabels]
    value=[val.text for val in rinfo]
    #add in the prep times
    recipe.update(dict(zip(label,value)))   

    #--------------------------------------------
    #--------grab nutritional data---------------
    #--------------------------------------------

    # Find the <th> element with the specified class
    th_element = soup.find('thead', class_='mntl-nutrition-facts-label__table-head')
    soup_head = th_element
    # Check if the <th> element was found

    # Find the <th> element with the specified class
    th_element = soup.find('thead', class_='mntl-nutrition-facts-label__table-head')
    soup_head = th_element
    # Check if the <th> element was found
    # Find the <span> element within the <th> element
    span_element = soup_head.find_all('span')
    # Check if the <span> element was found

    #2nd and 4th element are the data values
    recipe[span_element[0].text.strip()]=span_element[1].text.strip()
    recipe[span_element[2].text.strip()]=span_element[3].text.strip()


    td_element = soup.find('tbody', class_="mntl-nutrition-facts-label__table-body type--cat")
    soup_body = td_element

    #------------grab the nutrition table data------------------

    # Find the <td> element
    element = soup_body.find_all('tr')

    for el in element:
        nlabel= el.find('span')
        if nlabel:
            nvalue=el.find_next('td')
            nvalue=nvalue.text.strip().splitlines()
            recipe[nvalue[0]]=nvalue[1]

    soup.find('span', class_="mntl-nutrition-facts-label__table-body type--cat")
    #--------------------------------------------
    #-------------grab review data---------------
    #--------------------------------------------
    # Find the <div> element with the rating
    rating_div = soup.find('div', class_='comp type--squirrel-bold mntl-recipe-review-bar__rating mntl-text-block')

    # Find the <div> element with the rating count
    count_div = soup.find('div', class_='comp type--squirrel mntl-recipe-review-bar__rating-count mntl-text-block')

    # Extract the rating and count from the <div> elements
    rating = rating_div.text.strip()
    count = count_div.text.strip().strip('()')

    recipe['Average_Review'] = rating
    recipe['Review_Count'] = count
    
    rec_df = pd.DataFrame(recipe, index=[0])
    rec_df.to_csv(f'{rec_dir}\{rkey}_main.csv')
    #------------------------------------------
    #----------Build Ingredients Table---------
    #------------------------------------------
    # Find the <ul> element with the specified class
    ul_element = soup.find('ul', class_='mntl-structured-ingredients__list')

    # Check if the <ul> element was found
    if ul_element:
        # Find all <li> elements within the <ul> element
        li_elements = ul_element.find_all('li', class_='mntl-structured-ingredients__list-item')
        
        # Initialize lists to store extracted data
        quantities = []
        units = []
        ingredients = []
        
        # Iterate through the <li> elements and extract data
        for li in li_elements:
            span_quantity = li.find('span', {'data-ingredient-quantity': 'true'})
            span_unit = li.find('span', {'data-ingredient-unit': 'true'})
            span_ingredient = li.find('span', {'data-ingredient-name': 'true'})
            
            if span_quantity:
                quantities.append(span_quantity.text.strip())
            else:
                quantities.append('')
            
            if span_unit:
                units.append(span_unit.text.strip())
            else:
                units.append('')
            
            if span_ingredient:
                ingredients.append(span_ingredient.text.strip())
            else:
                ingredients.append('')
        
        # Print the extracted data
        temp_ing_df = pd.DataFrame({'id_recipe':rkey,'Quantity': quantities, 'Unit of Measure': units, 'Ingredient': ingredients})
        temp_ing_df.to_csv(f'{ing_dir}\{rkey}_ingredients.csv',index=False)
    else:
        print("The <ul> element with class 'mntl-structured-ingredients__list' was not found in the HTML.")

    
    #--------------------------------------------
    #--------------Grab Steps Data---------------
    #--------------------------------------------
    #grab steps data
    # Find the <th> element with the specified class
    steps = soup.find('ol', class_="comp mntl-sc-block-group--OL mntl-sc-block mntl-sc-block-startgroup")

    #
    step_desc=[]
    step_count=[]
    # Find the <td> element
    element = steps.find_all('li')
    c=1
    for el in element:
        par = el.find_all('p')
        step_desc.append("".join(p.text.strip() for p in par))
        step_count.append(c)
        c += 1

    temp_steps_df = pd.DataFrame({'id_recipe':rkey,'Step_Count': step_count, 'Step Description': step_desc})
    temp_steps_df.to_csv(f'{stp_dir}\{rkey}_steps.csv')
    return "some key that marks the list as done"

scrape_recipe()

