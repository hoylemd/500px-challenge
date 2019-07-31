import logging
from os import environ
from dataclasses import dataclass
from requests import get

from utils import prune_dict

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
            'image_size': 30,
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
        response = get(
            url,
            params={'consumer_key': self.key, 'image_size': 22},
        )
        logger.debug(f' -> HTTP {response.status_code}')

        return response
