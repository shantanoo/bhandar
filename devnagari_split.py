# Credits: https://stackoverflow.com/a/47123580/89346

import unicodedata


def split_clusters(txt):
    """ Generate grapheme clusters for the Devanagari text."""

    stop = '्'
    cluster = u''
    end = None

    for char in txt:
        category = unicodedata.category(char)
        if (category == 'Lo' and end == stop) or category == 'Mn':
            cluster = cluster + char
        else:
            if cluster:
                yield cluster
            cluster = char
        end = char

    if cluster:
        yield cluster
