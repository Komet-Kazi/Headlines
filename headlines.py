import feedparser
from flask import Flask
from flask import render_template


app = Flask(__name__)

# Dictionary of Rss urls and Publishers
RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'cnn': 'http://rss.cnn.com/rss/edition.rss',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}

# --------------------------------------------------------------------------------------- #
# pass variables through the url
@app.route('/')
@app.route('/<publication>')
def get_news(publication='bbc'):
    #TODO catch any invalid value passed via the url

    feed = feedparser.parse(RSS_FEEDS[publication])

    first_article = feed['entries'][0]

    # pass the entire list off articles from a publication into jinja
    rendered_page = render_template('home.html', publication=publication.upper(), articles=feed['entries'])

    return rendered_page


if __name__ == "__main__":
    app.run(port=5000, debug=True)
