import pytest
from unittest.mock import patch

from utils import prune_dict, make_pager_url
from five_hundred_px import FiveHundredPX


class TestUtils:
    def test_prune_dict(self):
        """Should remove ONLY the 'None' fields, not falsy"""
        raw = {
            'name': 'Darrow',
            'colour': 'Red',
            'fears': None,
            'tears': 0
        }

        assert prune_dict(raw) == {
            'name': 'Darrow',
            'colour': 'Red',
            'tears': 0
        }

    def test_make_pager_url(self):
        """Should return a properly formatted pager url"""
        assert make_pager_url(5, 2, 7) == '/?rpp=5&page=2'

    def test_make_pager_url__invalid_page(self):
        """Should return None, indicating no url to which to link"""
        assert make_pager_url(5, 12, 7) is None


class TestFiveHundredPX:
    def test_construct(self):
        """Should initialize with provided values"""
        api = FiveHundredPX(key='sesame', host='excels.io')
        assert api.key == 'sesame'
        assert api.host == 'excels.io'

    def test_construct__from_env(self, monkeypatch):
        """Should pull key from env"""
        monkeypatch.setenv('API_KEY', 'orion')
        api = FiveHundredPX()

        assert api.key == 'orion'

    def test_construct__no_key(self, monkeypatch):
        """Should raise an error"""

        monkeypatch.delenv('API_KEY')
        with pytest.raises(KeyError):
            FiveHundredPX()

    def test_get_feed(self):
        """Should construct request as expected"""
        api = FiveHundredPX(key='secret123', host='cheer.io')
        with patch('five_hundred_px.get', status_code=200) as get_mock:
            api.get_feed(rpp=7, page=2)

        get_mock.assert_called_with(
            'https://cheer.io/v1/photos',
            params={
                'feature': 'popular',
                'consumer_key': 'secret123',
                'rpp': 7,
                'page': 2
            }
        )

    def test_get_detail(self):
        """Should construct request as expected"""
        pass
