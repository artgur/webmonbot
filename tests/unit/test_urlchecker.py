import pytest
import responses
from webmonbot.urlchecker import URLChecker


class TestUrlChecker:

    @responses.activate
    def test_check_have_substring(self):
        params = {
            "url": 'http://havestring.com',
            "substring": 'needed string'
        }
        responses.add(
            responses.GET,
            params['url'],
            params['substring']
        )
        checker = URLChecker(**params)
        result = checker.check()
        assert result

    @responses.activate
    def test_check_dont_have_substring(self):
        params = {
            "url": 'http://donthavestring.com',
            "substring": 'needed string'
        }
        responses.add(
            responses.GET,
            params['url'],
            'missed string'
        )
        checker = URLChecker(**params)
        result = checker.check()
        assert not result