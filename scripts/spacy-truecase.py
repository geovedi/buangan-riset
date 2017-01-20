# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io
import re
import plac
import spacy
import bz2

import logging
logging.basicConfig(
    format='%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)


def preprocess(text):
    text = re.sub('„', '"', text)
    text = re.sub('“', '"', text)
    text = re.sub('”', '"', text)
    text = re.sub('–', '--', text)
    text = re.sub('—', '--', text)
    text = re.sub('´', "'", text)
    text = re.sub('‘', '"', text)
    text = re.sub('’', '"', text)
    text = re.sub("''", '"', text)
    text = re.sub('´´', '"', text)
    text = re.sub('…', '...', text)
    text = re.sub('«', '"', text)
    text = re.sub('«', '"', text)
    text = re.sub('«', '"', text)
    text = re.sub('»', '"', text)
    text = re.sub('»', '"', text)
    text = re.sub('»', '"', text)
    text = re.sub(r'([a-z])‘([a-z])', r'\1\'\2', text)
    text = re.sub(r'([a-z])’([a-z])', r'\1\'\2', text)
    text = re.sub(r'(\d+) - (\d+)', r'\1-\2', text)
    text = re.sub(r'(\d+) -(\d+)', r'\1-\2', text)
    text = re.sub(r'(\d+)- (\d+)', r'\1-\2', text)
    text = re.sub(r'([a-z])(\.)([A-Z])', r'\1\2 \3', text)
    text = text.replace(' - ', ' -- ')
    text = text.replace(';', '; ')
    text = re.sub(r'(.)\1{4,}', r'\1\1\1', text)
    return ' '.join(text.split())

def read_file(loc):
    if loc.endswith('.bz2'):
        input_stream = bz2.BZ2File(loc)
        must_decode = True
    else:
        input_stream = io.open(loc, 'r', encoding='utf-8')
        must_decode = False
    for line in input_stream:
        text = line.strip()
        if must_decode:
            text = text.decode('utf-8')
        text = preprocess(text)
        if text:
            yield text


def main(lang, input_file, output_file):
    nlp = spacy.load(lang)

    with io.open(output_file, 'w', encoding='utf-8') as out:
        for line_no, text in enumerate(read_file(input_file)):
            doc = nlp(text)
            doc = nlp(''.join([w.text_with_ws.lower() if w.pos_ != 'PROPN' else w.text_with_ws  for w in doc]))
            text = ' '.join([w.orth_ for w in doc])
            out.write(text)
            out.write('\n')

            if line_no % 10000 == 0:
                logging.info('Processed line: {}'.format(line_no))
        logging.info('Processed line: {}'.format(line_no))

if __name__ == '__main__':
    plac.call(main)
