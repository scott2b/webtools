"""
Query formations for web search. Generally good for common search engines. For
more Twitter-specific formations, see the Infolab context project query formations:
https://github.com/NUinfolab/context/blob/master/context/query.py
"""

from itertools import product, zip_longest

"""
From: https://docs.python.org/3.6/library/itertools.html#itertools.combinations
"""
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class QueryBuilder(object):

    _and = ' & '
    _or = ' | '
    _quote ='"'

    def quote(self, term):
        if ' ' in term:
            return '%s%s%s' % (self._quote, term, self._quote)
        else:
            return term

    def join(self, terms, parens=True):
        """
        >>> q.join(("1", "2", "3 three"))
        '(1 & 2 & "3 three")'
        >>> q.join(("1", "2", "3 three"), parens=False)
        '1 & 2 & "3 three"'
        >>> q._and = ' AND '
        >>> q.join(("1", "2", "3 three"))
        '(1 AND 2 AND "3 three")'
        >>> q.join(("1", "2", "3 three"), parens=False)
        '1 AND 2 AND "3 three"'
        """
        r = self._and.join([self.quote(t) for t in terms if t])
        if parens and len(terms) > 1:
            r = '(%s)' % r
        return r

    def disjoin(self, terms, parens=True):
        """
        >>> q.disjoin(("1", "2", "3 three"))
        '(1 | 2 | "3 three")'
        >>> q.disjoin(("1", "2", "3 three"), parens=False)
        '1 | 2 | "3 three"'
        >>> q._or = ' OR '
        >>> q.disjoin(("1", "2", "3 three"))
        '(1 OR 2 OR "3 three")'
        >>> q.disjoin(("1", "2", "3 three"), parens=False)
        '1 OR 2 OR "3 three"'
        """
        r = self._or.join([self.quote(t) for t in terms if t])
        if parens and len(terms) > 1:
            r = '(%s)' % r
        return r

    def anded_or_group_queries(self, term_list_1, n1, term_list_2, n2):
        """
        >>> q.anded_or_group_queries(['1','2','3','4'], 3, ['5','6','7'], 2)
        ['(1 | 2 | 3) & (5 | 6)', '(1 | 2 | 3) & (7)', '(4) & (5 | 6)', '(4) & (7)']
        """
        l1 = grouper(term_list_1, n1)
        l2 = grouper(term_list_2, n2)
        return ['%s%s%s' % (self.disjoin(t1), self._and, self.disjoin(t2))
            for t1, t2 in product(l1, l2)]


if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'q': QueryBuilder()})
