import logging
from dataclasses import dataclass
from os import environ
from requests import get
from flask import Flask, render_template, request

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)


def make_pager_url(rpp=None, page=None, total=None):
    """Generate a url for a pager link, or None if the link would be invalid"""

    if total is None:
        raise ValueError('total is required')
    rpp = int(rpp)
    page = int(page)

    if page < 1:
        return None

    if page > total:
        return None

    rpp_section = f"rpp={rpp}" if rpp else ''
    page_section = f"page={page}" if page else ''

    if rpp_section and page_section:
        return f"/?{rpp_section}&{page_section}"
    elif rpp_section or page_section:
        return f"/?{rpp_section}{page_section}"
    return f"/"


def prune_dict(obj):
    """Remove any None elements from the dict"""
    return {k: v for k, v in obj.items() if v is not None}


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


@app.route('/')
def index():
    rpp = request.args.get('rpp', None)
    page = request.args.get('page', None)

    api = FiveHundredPX()
    response = api.get_feed(rpp=rpp, page=page)

    raw = response.json()
    pages = raw['total_pages']
    photos = raw['photos']

    rpp = int(rpp or '50')
    page = int(page or '1')

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
