import logging
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

CACHE_DIR = './cache'
URL_PREFIX = 'http://localhost/content'


def replace_image_urls(obj):
    image = obj['images'][0]
    url = f"{URL_PREFIX}/{obj['id']}.{image['format']}"
    image['url'] = url
    image['https_url'] = url

    return obj


@app.route('/v1/photos/')
def list():
    rpp = int(request.args.get('rpp', 20))
    page = int(request.args.get('page', 1))

    lower_bound = (page - 1) * rpp
    upper_bound = lower_bound + rpp

    logger.debug(
        f"requested p{page} (rpp={rpp}), which is {lower_bound}-{upper_bound}"
    )

    with open(f"{CACHE_DIR}/list.json") as fp:
        all_photos = json.loads(fp.read())

    page_photos = all_photos[lower_bound:upper_bound]

    mocked_photos = [replace_image_urls(p) for p in page_photos]
    return jsonify({
        'current_page': page,
        'total_pages': 3,
        'total_items': 3 * 8,
        'photos': mocked_photos
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
