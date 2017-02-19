# -*- coding: utf-8 -*-
# This's just a dirty hack until Matthew merge `tokens.doc.noun_chunks()` to master branch.

from __future__ import unicode_literals

import plac
import io
from spacy.en import English
from spacy.parts_of_speech import NOUN
import logging
logging.basicConfig(format='%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

nlp = English()

labels = ['nsubj', 'dobj', 'nsubjpass', 'pcomp', 'pobj', 'conj', 'attr']
np_deps = [nlp.vocab.strings[label] for label in labels]

def extract_np(doc):
    for i in range(len(doc)):
        word = doc[i]
        if word.pos == NOUN and word.dep in np_deps:
            np = map(lambda x: doc[x].string, range(word.left_edge.i, word.i))
            np = ''.join(np)
            if len(np) > 0:
                yield np.strip()

def main(prefix, filelist, output):
    with io.open(output, 'w', encoding='utf-8') as out:
        for i, fname in enumerate(io.open(filelist, 'r', encoding='utf-8')):
            fname = fname.strip()
            doc = io.open('{0}/{1}'.format(prefix, fname), 'r', encoding='utf-8').read()
            spacy_doc = nlp(doc)
            for np in extract_np(spacy_doc):
                out.write('{0}\n'.format(np))
            logging.info((i, fname))

if __name__ == '__main__':
    plac.call(main)

