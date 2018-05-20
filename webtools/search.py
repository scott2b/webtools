import datetime
import requests
import time


class BingWebPage(dict):

    """
    No real attempt is made to stylize or format the full snippet or full rich
    caption (below). These are primarily useful for preliminary inspection of
    web page content, not so much for e.g. user interface display
    """
    def get_full_snippet(self):
        snippets = [link.get('snippet', '').strip() for link in
            self.get('deepLinks',[]) if link.get('snippet', '').strip()]
        return '\n'.join([self.get('snippet', '')] + snippets)

    """
    The richCaption parameter does not seem to be documented in Azure
    documentation. Use with caution.
    """
    def get_full_richcaption_description(self):
        descriptions = [section.get('description', '').strip() for section in
            self.get('richCaption', {}).get('sections', [])
            if section.get('description', '').strip()]
        return '\n'.join(descriptions)


class BingSearcher(object):

    SEARCH_URL = "https://api.cognitive.microsoft.com/bing/v7.0/search"

    def __init__(self, bing_api_key, rate_limit=3):
        self._api_key = bing_api_key
        self._rate_limit = rate_limit # calls per second
        self._rate = 1 / rate_limit
        self._last_search_time = None
        self._last_results = {}

    def search(self, query, count=50, offset=0):
        if self._last_search_time is not None:
            now = datetime.datetime.now()
            delta = (now - self._last_search_time).total_seconds()
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
        self._last_search_time = datetime.datetime.now()
        data = response.json()
        self._last_results = data
        return data

    def last_search_pages(self):
        return (BingWebPage(page) for page in
            self._last_results.get('webPages', {}).get('value', []))
