import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import requests
import urllib.parse


app = Flask(__name__)

# Dictionary of Rss urls and Publishers
RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'}

# --------------------------------------------------------------------------------------- #

@app.route('/')
def get_news():
    '''
    example url: http://127.0.0.1:5000/?publication=bbc
    params:
        publication -> name of rss feed publisher
        valid values: bbc, cnn, fox, iol
    returns:
        If the value is in our RSS_FEEDS dict, we return the matching publication headlines page.
    '''
    query = request.args.get('publication')

    if not query or query.lower() not in RSS_FEEDS:
        publication = 'bbc'
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    weather = get_weather('London,UK')

    return render_template('home.html', articles=feed['entries'], weather=weather)

def get_weather(query):
    query = urllib.parse.quote(query)  # Encode the query for a url
    url = f'http://api.openweathermap.org/data/2.5/weather?q={query}&units=metric&appid=01b39def802d744725886f7476405653'
    data = requests.get(url)
    parsed = data.json()
    weather = None
    if parsed.get('weather'):
        weather = {'description':
        parsed['weather'][0]['description'],
        'temperature': parsed['main']['temp'],
        'city': parsed['name']
        }
    return weather


    uel =api
if __name__ == "__main__":
    app.run(port=5000, debug=True)
