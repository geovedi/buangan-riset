# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io
from nltk.tag.util import str2tuple, tuple2str


def fix(corpus_ud, corpus_itb, corpus_out):
    itb = map(lambda tagged: map(str2tuple, tagged.split()),
              io.open(corpus_itb, 'r', encoding='utf-8').read().strip().split('\n'))
    ud = map(lambda tagged: map(str2tuple, tagged.split()),
             io.open(corpus_ud, 'r', encoding='utf-8').read().strip().split('\n'))

    corpus = []
    for x, y in zip(ud, itb):
        sent = []
        for xx, yy in zip(x, y):
            xx, yy = list(xx), list(yy)
            if xx[1] == 'PROPN':
                yy[1] = 'E--'
            if 'X--' in yy[1] or 'F--' in yy[1]:
                if xx[1] == 'NOUN':
                    yy[1] = yy[1].replace('X--', 'NSD').replace('F--', 'NSD')
                elif xx[1] == 'VERB':
                    yy[1] = yy[1].replace('X--', 'VSA').replace('F--', 'NSD')
                elif xx[1] == 'ADJ':
                    yy[1] = yy[1].replace('X--', 'ASP').replace('F--', 'ASP')
                elif xx[1] == 'ADV':
                    yy[1] = yy[1].replace('X--', 'D--').replace('F--', 'D--')
                elif xx[1] == 'ADP':
                    yy[1] = yy[1].replace('X--', 'R--').replace('F--', 'R--')
                elif xx[1] == 'DET':
                    yy[1] = yy[1].replace('X--', 'B--').replace('F--', 'B--')
            sent.append(tuple2str(yy))
        corpus.append(sent)

    with io.open(corpus_out, 'w', encoding='utf-8') as out:
        for sent in corpus:
            out.write(' '.join(sent))
            out.write('\n')

