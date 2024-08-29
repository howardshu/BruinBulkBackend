# scraper.py
import requests
import bs4
import numpy as np
import Constants

# TODO: add ability to show different days and separate meals
# aspects of the link include dining hall, day, meal


# returns a list of dining halls
def get_dining_halls():
    url = 'https://menu.dining.ucla.edu/hours/'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # list of dining hall names
    dining_halls = []

    for hall in soup.select('td.hours-head > a:nth-child(3)'):
        if hall.getText() == "Menu":
            url = hall.get('href')
            dining_halls.append(url)

    return dining_halls


# returns a list of menu items to send to the API for display at frontend
# nutrition represented as dictionary
def get_menu_for_api(hall_url):
    response = requests.get(hall_url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # empty list
    menu_items = []

    # TODO: possibly just send nutrition link to frontend without specific info?
    for item in soup.select('.recipelink'):
        nutrition_url = item.get('href')

        # Get nutritional facts from the item page
        food_name, nutrition_tags = get_nutrition_facts(nutrition_url)
        nutrition_dict = {}

        for item in nutrition_tags:
            info_str = item.getText().strip() # remove leading and trailing spaces
            if info_str[-1] == '%': # remove the % DV part of the string if it exists
                temp = info_str.rsplit(' ', 1)
                info_str = temp[0]
            info_list = info_str.rsplit(' ', 1)
            nutrition_dict[info_list[0]] = info_list[1]

        dictionary = {'name': food_name, 'nutrition': nutrition_facts}
        menu_items.append(dictionary)

    return menu_items


# returns a dictionary with the food name as the key and np array representing nutrition as value
# for backend calculation
def get_menu_nutrition(hall_url):
    response = requests.get(hall_url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    # empty dictionary
    menu_items = {}

    for item in soup.select('.recipelink'):
        nutrition_url = item.get('href')

        # Get nutritional facts from the item page
        food_name, nutrition_tags = get_nutrition_facts(nutrition_url)
        # empty array (see Constants.py)
        nutrition_facts = np.zeros(14)

        for item in nutrition_tags:
            info_str = item.getText().strip()
            if info_str[-1] == '%':
                temp = info_str.rsplit(' ', 1)
                info_str = temp[0]
            info_list = info_str.rsplit(' ', 1)
            idx = Constants.INDICES[info_list[0]]
            info_list[1] = info_list[1].replace(Constants.UNITS[idx], '')
            try:
                nutrition_facts[idx] = float(info_list[1])
            except ValueError:
                nutrition_facts[idx] = -1
        # TODO: better deal with unavailable items

        menu_items[food_name] = nutrition_facts

    return menu_items


# Return the name and a set of HTML tags with nutrition information
def get_nutrition_facts(nutrition_url):
    # Retrieve HTML and create bs4 element
    response = requests.get(nutrition_url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    name = soup.select('h2')
    serv_size_tags = soup.select('.nfserv')
    serv_size_str = serv_size_tags[0].getText()

    serv_size_str = serv_size_str.replace("&nbsp;", " ")

    food_name = name[0].getText() + ' ' + serv_size_str

    calorie_info = soup.select('.nfcal')
    nutrient_info = soup.select('.nfnutrient')
    all_info = calorie_info + nutrient_info
    # TODO: add calcium, potassium, iron, vitamin D functionality

    return food_name, all_info


# Test usage
"""
halls = get_dining_halls()
for hall in halls:
    print(hall)
    menu = get_menu_for_hall(Constants.LINK + hall)
    for key, value in menu.items():
        print(key)
        print(value)
    print()
"""