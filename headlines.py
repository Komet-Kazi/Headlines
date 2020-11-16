import feedparser
from flask import Flask
from flask import render_template
from flask import request
import json
import requests
import urllib.parse

# ----------------- Use secrets.ini file to store private info and passwords ---------------------#
import configparser

config = configparser.ConfigParser()
config.read('secrets.ini')

OWM_APP_ID = config['OpenWeatherMap']['API_KEY']
OER_APP_ID = config['OpenExchangeRates']['API_KEY']
# --------------------------------------------------------------------------------------- #
# logging configuration

import http
import logging
from pathlib import Path

# The path to the directory where this file is saved
CURRENT_DIRECTORY = Path(__file__).parent

# The path/file to send logs too (so file extension is .log not .py.log)
LOG_LOCATION = CURRENT_DIRECTORY.joinpath(f'{Path(__file__).stem}.log')

# Configure logging to file
logging.basicConfig(level='DEBUG', filename=LOG_LOCATION, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# Changing the logging debug level greater than 0 will log the response HTTP headers to stdout.
# useful if you're dealing with an API that returns a large body payload that is not suitable for logging or contains binary content.
http.client.HTTPConnection.debuglevel = 1
# --------------------------------------------------------------------------------------- #

app = Flask(__name__)

# Dictionary of Rss urls and Publishers
RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'}

# --------------------------------------------------------------------------------------- #

DEFAULT = {'publication': 'bbc', 'city': 'Tucson,US', 'currency_from':'USD', 'currency_to':'JOD' }


@app.route('/')
def home():
    '''

    '''
    # Get customized headlines based  on user input or DEFAULT
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULT['publication']
    articles = get_news(publication)

    # Get customized weather based on user iput or DEFAULT
    city = request.args.get('city')
    if not city:
        city = DEFAULT['city']
    weather = get_weather(city)

    # get customized currency rates via user input or DEFAULT
    currency_from = request.args.get('currency_from')
    if not currency_from:
        currency_from = DEFAULT['currency_from']

    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULT['currency_to']

    rate, currencies = get_rate(currency_from, currency_to)
    currency_exchange = {
        'rate': rate,
        'from': currency_from,
        'to': currency_to
    }
    return render_template('home.html', articles=articles, weather=weather, currency_exchange=currency_exchange, currencies=currencies)


def get_news(query):
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
        publication = DEFAULT['publication']
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])

    return feed['entries']

def get_weather(query):
    '''
    Request current weather information for the location passed.
    Params:
        query --> string in the format: '{city},{state_code},{country_code}'
                state_code is only accepted for US Locations
                country_code defaults to US if not specified
        Returns:
        weather --> Dictionary containing city name, temperature, description
    '''
    query = urllib.parse.quote(query)  # Encode the query for a url
    url = f'http://api.openweathermap.org/data/2.5/weather?q={query}&units=imperial&appid={OWM_APP_ID}'

    data = requests.get(url)
    json_response = data.json()

    logging.debug('json response:\n' + jPrint(json_response))
    weather = None

    if json_response.get('weather'):
        weather = {
            'description': json_response['weather'][0]['description'],
            'temperature': json_response['main']['temp'],
            'city': json_response['name'],
            'country_code': json_response['sys']['country']
        }

    return weather

def get_rate(frm, to):
    '''
    Request current exchange rate information for the location passed.
    Params:
        frm --> Starting Currency Code
        to -->Ending Currency Code
        Returns:
            conversion rate -->
    '''

    url = f'https://openexchangerates.org//api/latest.json?app_id={OER_APP_ID}'

    response = requests.get(url)
    all_currency = response.json()
    rates = all_currency.get('rates')

    logging.debug('json response:\n' + jPrint(rates))

    frm_rate = rates.get(frm.upper())
    to_rate = rates.get(to.upper())

    return (to_rate/frm_rate, rates.keys())

def jPrint(obj):
    '''
    Convert a json object into a formatted string with sorted keys
    Params:
        obj --> json object
    Returns:
        formated string
    '''

    return json.dumps(obj, sort_keys=True, indent=4)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
