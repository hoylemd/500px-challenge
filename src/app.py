import os
import logging
from flask import Flask, request, jsonify

from five_hundred_px import FiveHundredPX

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

DEFAULT_HOST = 'https://api.500px.com'
try:
    API_KEY = os.environ['API_KEY']
except KeyError as exc:
    raise KeyError(
        'No `API_KEY` env var available.'
    ) from exc


@app.route('/bff/')
def index():
    rpp = int(request.args.get('rpp', 8))
    page = request.args.get('page', None)

    logger.debug(f'requesting list page {page} with rpp {rpp}')

    api_host = os.environ.get('API_HOST', DEFAULT_HOST)
    api = FiveHundredPX(key=API_KEY, host=api_host)
    response = api.get_feed(rpp=rpp, page=page)

    raw = response.json()

    return jsonify(raw)


@app.route('/bff/<int:photo_id>')
def detail(photo_id):

    api_host = os.environ.get('API_HOST', DEFAULT_HOST)
    api = FiveHundredPX(key=API_KEY, host=api_host)
    raw = api.get_detail(photo_id).json()

    return jsonify(raw)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
