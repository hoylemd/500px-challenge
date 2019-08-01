import logging
from flask import Flask, request, jsonify

from five_hundred_px import FiveHundredPX

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


@app.route('/bff/')
def index():
    rpp = int(request.args.get('rpp', 8))
    page = request.args.get('page', None)

    api = FiveHundredPX()
    response = api.get_feed(rpp=rpp, page=page)

    raw = response.json()

    return jsonify(raw)


@app.route('/bff/<int:photo_id>')
def detail(photo_id):

    api = FiveHundredPX()
    raw = api.get_detail(photo_id).json()

    return jsonify(raw)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
