# app.py
from flask import Flask, render_template
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://mongo:27017/')  # 'mongo' is the hostname of the MongoDB container
db = client['web_scraper_db']
collection = db['gamestop_data']

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

# Route to scrape and display GameStop data
@app.route('/')
def index():
    # Scrape data and store in MongoDB
    games_data = scrape_gamestop()
    collection.insert_many(games_data)

    # Fetch data from MongoDB
    games_from_db = collection.find()

    # Render template with scraped data
    return render_template('index.html', games=games_from_db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
