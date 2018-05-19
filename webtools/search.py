import datetime
import requests
import time


class BingSearcher(object):

    SEARCH_URL = "https://api.cognitive.microsoft.com/bing/v7.0/search"

    def __init__(self, bing_api_key, rate_limit=3):
        self._api_key = bing_api_key
        self._rate_limit = rate_limit # calls per second
        self._rate = 1 / rate_limit
        self._last_search = None

    def search(self, query, count=50, offset=0):
        if self._last_search is not None:
            delta = (datetime.datetime.now() - self._last_search).total_seconds()
            delay = self._rate - delta
            if delay > 0:
                time.sleep(delay)
        headers = {"Ocp-Apim-Subscription-Key" : self._api_key}
        params  = {
            'q': query,
            'textDecorations':False,
            'textFormat':'HTML',
            'count': count, # max 50 default 10
            'offset': offset
        }
        response = requests.get(self.SEARCH_URL, headers=headers, params=params)
        response.raise_for_status()
        self._last_search = datetime.datetime.now()
        return response.json()

