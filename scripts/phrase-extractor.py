# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import plac
import codecs
import regex as re
from types import StringType
from nltk.align.phrase_based import phrase_extraction
from collections import defaultdict

def read_file(fname):
    return codecs.open(fname, 'r', 'utf-8').read().strip().split('\n')

def convert_alignment(a):
    return map(lambda x: tuple(map(lambda y: int(y), x.split('-'))), a.split())

def postclean(text):
    return text.replace(u'\u200b', '')

def whitespace_tokenizer(text):
    return re.sub(r'\s+', ' ', postclean(text)).split()


@plac.annotations(
    source_file=plac.Annotation("Source file", 'option', 's', str),
    target_file=plac.Annotation("Target file", 'option', 't', str),
    aligment_file=plac.Annotation("Alignment file", 'option', 'a', str),
    output_file=plac.Annotation("Output file", 'option', 'o', str),
    max_ngram=plac.Annotation("Max N-gram length", 'option', 'm', int)
)
def main(source_file, target_file, aligment_file, output_file, max_ngram=5):
    assert source_file and target_file and aligment_file and output_file, 'missing arguments'

    sources = read_file(source_file)
    targets = read_file(target_file)
    alignments = map(convert_alignment, read_file(aligment_file))

    assert len(sources) == len(targets) == len(alignments), 'unequal length'

    phrases = defaultdict(int)

    for x, y, z in zip(sources, targets, alignments):
        for i, j, a, b in sorted(phrase_extraction(x, y, z)):
            a, b = whitespace_tokenizer(a), whitespace_tokenizer(b)
            if 1 <= len(a) <= max_ngram and 1 <= len(b) <= max_ngram:
                phrases[(' '.join(a), ' '.join(b))] += 1

    with codecs.open(output_file, 'w', 'utf-8') as out:
        for (a, b), c in phrases.iteritems():
            out.write('{0}\t{1} ||| {2}\n'.format(c, a, b))

if __name__ == '__main__':
    plac.call(main)
