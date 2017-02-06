#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import re
import io
import plac
import spacy


def read_file(loc):
    must_decode = True
    if loc.endswith('.bz2'):
        import bz2
        input_stream = bz2.BZ2File(loc)
    elif loc.endswith('.gz'):
        import gzip
        input_stream = gzip.GzFile(loc)
    else:
        input_stream = io.open(loc, 'r', encoding='utf-8')
        must_decode = False

    for line in input_stream:
        text = line.strip()
        if text:
            if must_decode:
                text = text.decode('utf-8')
            yield preprocess(text)


def preprocess(text):
    text = re.sub(r'([a-z])‘([a-z])', r'\1\'\2', text)
    text = re.sub(r'([a-z])’([a-z])', r'\1\'\2', text)
    text = re.sub(r'''([„“”‘’«»]|''|``)''', '"', text)
    text = re.sub(r'''([–—]|--| - )''', ' -- ', text)
    text = re.sub('´', "'", text)
    text = re.sub('…', '...', text)
    text = re.sub(r'(\d+) - (\d+)', r'\1-\2', text)
    text = re.sub(r'(\d+) -(\d+)', r'\1-\2', text)
    text = re.sub(r'(\d+)- (\d+)', r'\1-\2', text)
    text = re.sub(r'([a-z])(\.)([A-Z])', r'\1\2 \3', text)
    text = re.sub(r'(.)\1{4,}', r'\1\1\1', text)
    text = re.sub(r'[\u202c\u202d]', ' ', text)
    text = text.replace(';', '; ')
    text = text.replace("' s ", "'s ")
    return ' '.join(text.split())


def repr_word(word):
    text = word.text
    if word.pos_ != 'PROPN':
        return text.lower()
    return text


def main(lang, input_file, output_file):
    nlp = spacy.load(lang)

    with io.open(output_file, 'w', encoding='utf-8') as out:
        text = ''
        for i, text in enumerate(read_file(input_file)):
            out.write(' '.join(repr_word(t) for t in nlp(text)))
            out.write('\n')


if __name__ == '__main__':
    plac.call(main)
