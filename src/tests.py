from utils import prune_dict, make_pager_url


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
        pass

    def test_construct__from_env(self):
        """Should pull key from env"""
        pass

    def test_construct__no_key(self):
        """Should raise an error"""
        pass

    def test_get_feed(self):
        """Should construct request as expected"""
        pass

    def test_get_detail(self):
        """Should construct request as expected"""
        pass
