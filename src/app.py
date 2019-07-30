import logging
from os import environ
from requests import get
from flask import Flask, render_template, request

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


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


@app.route('/')
def index():
    logger.info('acquiring config')
    api_key = environ.get('API_KEY', None)
    api_host = environ.get('API_HOST', 'api.500px.com')

    if api_key is None:
        raise ValueError('no API key supplied')

    rpp = request.args.get('rpp', None)
    page = request.args.get('page', None)
    logger.info(f"args acquired: rpp: {rpp}, page: {page})")
    url = f"https://{api_host}/v1/photos"
    params = prune_dict({
        'feature': 'popular',
        'consumer_key': api_key,
        'rpp': rpp,
        'page': page,
    })
    logger.info(f'params prepped: {params}, url: {url}')

    response = get(url, params=params)
    logger.info(f"--- GET {response.url}")

    rpp = int(rpp or '50')
    page = int(page or '1')

    raw = response.json()
    pages = raw['total_pages']
    photos = raw['photos']

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

    logger.info('rendering page...')
    return render_template('index.html', **context)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
