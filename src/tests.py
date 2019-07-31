class TestUtils:
    def test_prune_dict(self):
        """Should remove ONLY the 'None' fields, not falsy"""
        pass

    def test_make_pager_url(self):
        """Should return a properly formatted pager url"""
        pass

    def test_make_pager_url__invalid_page(self):
        """Should return None, indicating no url to which to link"""
        pass

    def test_make_pager_url__one_section(self):
        """Should return a url with only one queryparam"""
        pass


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
