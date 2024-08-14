# scraper.py
import requests
from bs4 import BeautifulSoup


def get_dining_hall_links():
    url = 'https://menu.dining.ucla.edu/hours/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    dining_halls = {}

    for link in soup.select('.dining-hall-card a'):
        hall_name = link.get_text().strip()
        hall_url = 'https://menu.dining.ucla.edu' + link['href']
        dining_halls[hall_name] = hall_url

    return dining_halls


def get_menu_for_hall(hall_url):
    response = requests.get(hall_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    menu_items = []

    for item in soup.select('.menu-item'):
        food_name = item.select_one('.recipename').get_text().strip()
        nutrition_url = 'https://menu.dining.ucla.edu' + item['href']

        # Get nutritional facts from the item page
        nutrition_facts = get_nutrition_facts(nutrition_url)

        menu_items.append({
            'name': food_name,
            'nutrition': nutrition_facts,
        })

    return menu_items


def get_nutrition_facts(nutrition_url):
    response = requests.get(nutrition_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    nutrition_facts = {}

    # Example: Extracting calorie information
    calorie_info = soup.find('span', text='Calories')
    if calorie_info:
        nutrition_facts['calories'] = calorie_info.find_next('span').get_text().strip()

    # Add more fields as needed
    # Example: Fat, Protein, Carbohydrates, etc.

    return nutrition_facts


# Example usage
dining_halls = get_dining_hall_links()
for hall_name, hall_url in dining_halls.items():
    print(f"Menu for {hall_name}:")
    menu = get_menu_for_hall(hall_url)
    for item in menu:
        print(f"- {item['name']}: {item['nutrition']}")