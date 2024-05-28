# app.py
from flask import Flask, render_template
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# MongoDB setup
client = MongoClient('mongodb://mongo:27017/')  # 'mongo' is the hostname of the MongoDB container
db = client['web_scraper_db']
collection = db['links']

# Web scraper function
def scrape_data():
    url = 'https://www.gamespot.com/'  # Replace with the URL of the website to scrape
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [link.get('href') for link in soup.find_all('a')]
    return links

# Route to scrape and display data
@app.route('/')
def index():
    # Scrape data and store in MongoDB
    links = scrape_data()
    collection.insert_many([{'link': link} for link in links])

    # Fetch data from MongoDB
    links_from_db = [doc['link'] for doc in collection.find()]

    # Render template with scraped data
    return render_template('index.html', links=links_from_db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
