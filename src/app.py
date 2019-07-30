import logging
from os import environ
from requests import get
from flask import Flask, render_template

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


@app.route('/')
def index():
    api_key = environ.get('API_KEY', None)
    api_host = environ.get('API_HOST', 'api.500px.com')

    if api_key is None:
        raise ValueError('no API key supplied')

    # get the first page
    url = f"https://{api_host}/v1/photos"
    params = {
        'feature': 'popular',
        'consumer_key': api_key,
    }

    response = get(url, params=params)
    logger.info(f"--- GET {response.url}")

    raw = response.json()
    photos = raw['photos']
    context = {
        'message': 'weeee',
        'photos': photos
    }
    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
