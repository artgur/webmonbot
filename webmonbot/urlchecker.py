import requests
import logging

logger = logging.getLogger(__name__)


class URLChecker:
    def __init__(self, url, substring):
        self.url = url
        self.substring = substring

    def check(self):
        with requests.session() as s:
            r = s.get(url=self.url)

        if self.substring in r.text and r.ok:
            return True
        else:
            return False
