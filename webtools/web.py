"""
tools for managing downloaded web resources
"""
import requests
import requests_cache
import uuid
try:
    from newspaper import Article
except ImportError:
    print('WARNING: Newspaper required for text extraction and summarization')
except ModuleNotFoundError:
    print('WARNING: Newspaper required for text extraction and summarization')

requests_cache.install_cache()


class WebPage(object):

    def __init__(self, url):
        self.url = url
        self._article = None
        self._html = None
        self._title = None
        self._text = None
        self._summary = None

    @property
    def html(self):
        """
        >>> p.html.strip()[:15]
        '<!DOCTYPE html>'
        """
        if self._html is None:
            self._html = requests.get(self.url).text
        return self._html

    @property
    def uuid(self):
        """
        >>> p.uuid
        UUID('09cdf8ef-e61c-308d-b53b-f549242041f8')
        """
        return uuid.uuid3(uuid.NAMESPACE_URL, self.url)

    @property
    def article(self):
        """This page as a Nespaper article object
        >>> isinstance(p.article, Article)
        True
        """
        if self._article is None:
            try:
                a = Article(self.url)
                a.set_html(self.html)
                a.parse()
                a.nlp()
                self._article = a
            except NameError:
                raise Exception(
                  'Newspaper is required for text extraction and summarization')
        return self._article

    @property
    def title(self):
        """
        >>> p.title
        'Test title'
        """
        if self._title is None:
            self._title = self.article.title
        return self._title

    @property
    def text(self):
        """
        >>> p.text
        'This is some test text.'
        """
        if self._text is None:
            self._text = self.article.text
        return self._text

    @property
    def summary(self):
        """
        >>> p.summary
        'This is some test text.'
        """
        if self._summary is None:
            self._summary = self.article.summary
        return self._summary


if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'p': WebPage('http://localhost:8000/test.html')})
