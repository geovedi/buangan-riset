#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io
import re
import plac
import spacy

import logging
logging.basicConfig(
    format='%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)


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


def postprocess(text):
    text = text.replace("' s ", "'s ")
    return text


def read_file(loc):
    if loc.endswith('.bz2'):
        import bz2
        input_stream = bz2.BZ2File(loc)
        must_decode = True
    elif loc.endswith('.gz'):
        import gzip
        input_stream = gzip.GzipFile(loc)
        must_decode = True
    else:
        input_stream = io.open(loc, 'r', encoding='utf-8')
        must_decode = False
    for line in input_stream:
        text = line.strip()
        if must_decode:
            text = text.decode('utf-8')
        text = preprocess(text)
        yield text


@plac.annotations(
    lang=plac.Annotation('Language', 'option', 'l', str),
    input_file=plac.Annotation('Input file', 'option', 'i', str),
    output_file=plac.Annotation('Output file', 'option', 'o', str),
    tokenize=plac.Annotation('Tokenize', 'flag', 't', bool),
)
def main(lang, input_file, output_file, tokenize=False):
    nlp = spacy.load(lang)

    def repr_word(word, tokenize=False):
        if tokenize:
            text = word.text
        else:
            text = word.text_with_ws
        if word.pos_ == 'DET':
            text = text.lower()
        elif word.pos_ != 'PROPN':
            text = text.lower()
        return text

    with io.open(output_file, 'w', encoding='utf-8') as out:
        for line_no, text in enumerate(read_file(input_file)):
            if tokenize:
                join = ' '.join
            else:
                join = ''.join
            text = join([repr_word(w, tokenize=tokenize)  for w in nlp(text)])
            out.write(postprocess(text))
            out.write('\n')

            if line_no % 10000 == 0:
                logging.info("processing line: {}".format(line_no))
        logging.info("processing line: {}".format(line_no))

if __name__ == '__main__':
    plac.call(main)
