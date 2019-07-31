import logging
from dataclasses import dataclass
from os import environ
from requests import get
from flask import Flask, render_template, request

from utils import prune_dict, make_pager_url

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


@dataclass
class FiveHundredPX:
    key: str = None
    host: str = 'api.500px.com'

    def __post_init__(self):
        if self.key is None:
            self.key = environ['API_KEY']

    def get_feed(self, feature='popular', rpp=None, page=None):
        url = f"https://{self.host}/v1/photos"
        params = prune_dict({
            'feature': 'popular',
            'consumer_key': self.key,
            'rpp': rpp,
            'page': page,
        })

        predicted_qs = '&'.join(
            f"{k}={v}" for k, v in params.items() if k != 'consumer_key'
        )
        logger.debug(f'Making GET request: {url}?{predicted_qs}')
        response = get(url, params=params)
        logger.debug(f' -> HTTP {response.status_code}')

        return response

    def get_detail(self, id):
        url = f"https://{self.host}/v1/photos/{id}"

        logger.debug(f'Making GET request: {url}')
        response = get(url, params={'consumer_key': self.key})
        logger.debug(f' -> HTTP {response.status_code}')

        return response


@app.route('/')
def index():
    rpp = int(request.args.get('rpp', 8))
    page = request.args.get('page', None)

    api = FiveHundredPX()
    response = api.get_feed(rpp=rpp, page=page)

    raw = response.json()
    pages = raw['total_pages']
    photos = raw['photos']

    page = int(page or 1)

    if page > pages:
        page = pages

    context = {
        'photos': photos,
        'n': len(photos),
        'rpp': rpp,
        'page': page,
        'pages': pages,
        'prev_link': make_pager_url(rpp=rpp, page=page - 1, total=pages),
        'next_link': make_pager_url(rpp=rpp, page=page + 1, total=pages)
    }

    return render_template('index.html', **context)


@app.route('/<int:photo_id>')
def detail(photo_id):

    api = FiveHundredPX()
    raw = api.get_detail(photo_id).json()

    context = {
        'photo': raw['photo']
    }

    return render_template('detail.html', **context)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
