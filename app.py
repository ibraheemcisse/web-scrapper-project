from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

# Web scraper function for GameStop website
def scrape_gamestop():
    url = 'https://www.gamestop.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    games = soup.find_all('div', class_='product-tile')

    game_data = []
    for game in games:
        title = game.find('div', class_='title').text.strip()
        price = game.find('div', class_='price').text.strip()
        rating = game.find('span', class_='rating').text.strip()
        description = game.find('div', class_='description').text.strip()

        game_info = {
            'title': title,
            'price': price,
            'rating': rating,
            'description': description
        }
        game_data.append(game_info)

    return game_data
