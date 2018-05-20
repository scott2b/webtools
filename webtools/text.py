"""
Text processing tools
"""
from collections import Counter
from textblob import TextBlob
import spacy

nlp = spacy.load('en')
default_stoplist = [t.text for t in nlp.vocab if t.is_stop]


"""
TextBlob doesn't deal well with curly quotes
"""
def prepare_text(text):
    text = text.replace("’", "__APOS__")
    text = text.replace("'", "__APOS__")
    text = text.replace('”', '"')
    text = text.replace('“', '"')
    return text


def render_text(text):
    return text.replace('__APOS__', "'")


class Text(object):

    def __init__(self, text):
        self._text = text
        self._blob = None

    @property
    def prepared_text(self):
        return prepare_text(self._text)

    @property
    def rendered_text(self):
        return render_text(self._text)

    @property
    def blob(self):
        if self._blob is None:
            self._blob = TextBlob(self.prepared_text)
        return self._blob

    """
    Within the iterable range of n_range, count up the grams, removing smaller
    grams that are included within larger, and return grams and counts in reverse
    order by count.

    Only applies stoplisting to end tokens (e.g. n1 and n3 for n == 3)
    """
    def ordered_ngrams(self, n_range, stoplist=default_stoplist, distill=True):
        """
        >>> [x for x,y in t.ordered_ngrams(range(2,4)) if y>1]
        ['reasons unknown', 'left unfinished', 'public works', 'works of Puncher', 'Puncher and Wattmann', 'unknown but time', 'time will tell', 'Testew and Cunard']
        """
        grams = {}
        for n in n_range:
            for gram in self.blob.ngrams(n=n):
                gram = [render_text(t) for t in gram]
                if gram[0].lower() not in stoplist \
                        and gram[-1].lower() not in stoplist:
                    gram = ' '.join(gram)
                    if gram not in grams:
                        grams[gram] = 0
                    grams[gram] += 1
        if distill:
            keys = [k for k in grams.keys()]
            for k1 in keys:
                for k2 in keys:
                    if k1 != k2 and k1 in k2:
                        if grams[k1] <= grams[k2]:
                            del(grams[k1])
                            break
                else:
                    continue
                break
        return sorted(grams.items(), key=lambda x: x[1], reverse=True)


    """
    Get the entities in the text reverse ordered by the number of matches
    in the text.

    label options are:
        PERSON NORP FACILITY ORG GPE LOC PRODUCT EVENT WORK_OF_ART LAW LANGUAGE
        DATE TIME PERCENT MONEY QUANTITY ORDINAL CARDINAL

    See Spacy docs for details:
    https://spacy.io/usage/linguistic-features#section-named-entities

    Returns a Counter object:
    https://docs.python.org/3.6/library/collections.html#counter-objects

    May return a dictionary in the future if Python 2 support is required
    """
    def scored_entities(self, exclude_labels=None):
        """
        >>> [x for x,y in t.scored_entities().most_common(3)]
        ['Testew', 'Puncher', 'Wattmann']
        >>> [x for x,y in t.scored_entities(exclude_labels=['PERSON']).most_common(3)]
        ['Puncher', 'Miranda', 'the Acacacacademy of Anthropopopometry']
        """
        exclude_labels = exclude_labels or []
        return Counter([e.text.strip() for e in nlp(self._text).ents if
            e.text.strip() and e.label_ not in exclude_labels])


test_text = """Given the existence as uttered forth in the public works of Puncher and Wattmann of a personal God quaquaquaqua with white beard quaquaquaqua outside time without extension who from the heights of divine apathia divine athambia divine aphasia loves us dearly with some exceptions for reasons unknown but time will tell and suffers like the divine Miranda with those who for reasons unknown but time will tell are plunged in torment plunged in fire whose fire flames if that continues and who can doubt it will fire the firmament that is to say blast hell to heaven so blue still and calm so calm with a calm which even though intermittent is better than nothing but not so fast and considering what is more that as a result of the labors left unfinished crowned by the Acacacacademy of Anthropopopometry of Essy­in­Possy of Testew and Cunard it is established beyond all doubt all other doubt than that which clings to the labors of men that as a result of the labors unfinished of Testew and Cunnard it is established as hereinafter but not so fast for reasons unknown that as a result of the public works of Puncher and Wattmann it is established beyond all doubt that in view of the labors of Fartov and Belcher left unfinished for reasons unknown of Testew and Cunard left unfinished ..."""

if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'t': Text(test_text)})
