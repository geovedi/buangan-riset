#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import bz2
import joblib
import plac
import os
import io
import re
from os import path
from toolz import partition
from preshed.counter import PreshCounter
from spacy.strings import StringStore
from joblib import Parallel, delayed

import logging
logging.basicConfig(
    format='%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)


def parallelize(func, iterator, n_jobs, extra, backend='multiprocessing'):
    extra = tuple(extra)
    return Parallel(n_jobs=n_jobs, backend=backend)(delayed(func)(*(item + extra)) for item in iterator)

def cleanup(text):
    text = text.replace('--', ' -- ')
    text = text.replace('">', ' "> ')
    text = text.replace('="', ' =" ')
    return text

def rep_text(text):
    if len(text) >= 50:
        return ' !LONGWORD! '
    return text


def read_file(loc):
    for line in bz2.BZ2File(loc):
        text = line.strip().decode('utf-8')
        if text:
            yield cleanup(text)


def process(batch_id, inputs, output_dir, lang, n_threads, batch_size, min_ngram, max_ngram):
    logging.info('Processing batch_id: {}'.format(batch_id))
    subtrees = PreshCounter()
    subtrees_string_map = StringStore()
    noun_chunks = PreshCounter()
    noun_chunks_string_map = StringStore()

    if lang.lower() == "en":
        from spacy.en import English
        NLU = English()
        NLU.matcher = None
    elif lang.lower() == "id":
        from spacy.id import Indonesian
        NLU = Indonesian()
        NLU.matcher = None

    for i, doc in enumerate(NLU.pipe(inputs, batch_size=batch_size, n_threads=n_threads)):
        phrases = set()
        for tok in doc:
            st_len = len(list(tok.subtree))
            if min_ngram <= st_len <= max_ngram:
                st = ''.join([rep_text(t.text_with_ws) for t in tok.subtree]).strip()
                orth = subtrees_string_map[st]
                subtrees.inc(orth, 1)
        for np in doc.noun_chunks:
            if min_ngram <= len(np) <= max_ngram:
                st = ''.join([rep_text(t.text_with_ws) for t in np]).strip()
                orth = noun_chunks_string_map[st]
                noun_chunks.inc(orth, 1)

        if i % batch_size == 0:
            logging.info('Processing batch_id: {}, doc: {}'.format(batch_id, i))

    output_fname = path.join(output_dir, 'batch{}.st.freq'.format(batch_id))
    with io.open(output_fname, 'w', encoding='utf-8') as out:
        for orth, count in subtrees:
            st = subtrees_string_map[orth]
            if count >= 5 and '!LONGWORD!' not in st:
                out.write('{}\t{}\n'.format(count, st))

    output_fname = path.join(output_dir, 'batch{}.np.freq'.format(batch_id))
    with io.open(output_fname, 'w', encoding='utf-8') as out:
        for orth, count in noun_chunks:
            if count >= 5:
                st = noun_chunks_string_map[orth]
                out.write('{}\t{}\n'.format(count, st))


@plac.annotations(
    input_fname=plac.Annotation("Input filename", 'option', 'i', str),
    output_dir=plac.Annotation("Output dir", 'option', 'o', str),
    lang=plac.Annotation('Language', 'option', 'l', str),
    n_process=plac.Annotation("Num process", 'option', 'p', int),
    n_threads=plac.Annotation("Num threads", 'option', 't', int),
    batch_size=plac.Annotation("Batch size", 'option', 'b', int),
    min_ngram=plac.Annotation("Min N-Gram", 'option', 'N', int),
    max_ngram=plac.Annotation("Max N-Gram", 'option', 'M', int),
)
def main(input_fname, output_dir, lang="EN", n_process=2, n_threads=4, batch_size=1000, min_ngram=3, max_ngram=6):
    if n_process >= 2:
        texts = partition(500000, read_file(input_fname))
        parallelize(process, enumerate(texts), n_process,
                    [output_dir, lang, n_threads, batch_size, min_ngram, max_ngram],
                    backend='multiprocessing')
    else:
        process(0, read_file(input_fname), output_dir, lang,
                n_threads, batch_size, min_ngram, max_ngram)



if __name__ == '__main__':
    plac.call(main)
