import logging
from flask import Flask, render_template, request

from utils import make_pager_url
from five_hundred_px import FiveHundredPX

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


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
