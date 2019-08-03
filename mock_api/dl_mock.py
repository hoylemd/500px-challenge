import re
import os
import json
import logging
from requests import get
import argparse

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


API_URL = 'https://api.500px.com/v1/photos'
CACHE_DIR = './cache'


def write_json(path, blob):
    with open(path, 'w') as fp:
        fp.write(json.dumps(blob, indent=4, separators=(',', ':')))


def dl_photo(id, api_key):
    url = f"{API_URL}/{id}"
    logger.info(f'downloading image {id}...')
    raw = get(url, params={'api_key': api_key}).json()
    write_json(f"{CACHE_DIR}/{id}.json", raw['photo'])
    image = raw['photo']['images'][0]
    image_resp = get(image['https_url'])
    with open(f"{CACHE_DIR}/{id}.{image['format']}", 'wb') as fp:
        fp.write(image_resp.content)


def main(rpp, pages):
    try:
        api_key = os.environ['API_KEY']
    except KeyError:
        with open('../.env') as fp:
            for line in fp.readlines():
                matches = re.match(r'^API_KEY ?= ?([a-zA-Z0-9]+)$', line)
                if matches:
                    api_key = matches.groups(1)
                    break

    if not api_key:
        raise Exception('No API key detected')

    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    total_reqs = rpp * pages

    response = get(API_URL, params={
        'consumer_key': api_key,
        'rpp': total_reqs
    })

    photos = response.json()['photos']

    write_json(f"{CACHE_DIR}/list.json", photos)

    for photo in photos:
        dl_photo(photo['id'], api_key)


def _args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rpp', '-r', type=int, default=8, required=False)
    parser.add_argument('--pages', '-p', type=int, default=3, required=False)
    return parser.parse_args()


if __name__ == '__main__':
    args = _args()
    main(rpp=args.rpp, pages=args.pages)
