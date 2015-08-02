# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import plac
import codecs
import regex as re
from types import StringType
from collections import defaultdict

import logging
logging.basicConfig(format='%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def read_file(fname):
    return codecs.open(fname, 'r', 'utf-8').read().strip().split('\n')

def convert_alignment(a):
    return map(lambda x: tuple(map(lambda y: int(y), x.split('-'))), a.split())

def postclean(text):
    return text.replace(u'\u200b', '')

def whitespace_tokenizer(text):
    return re.sub(r'\s+', ' ', postclean(text)).split()

def phrase_extraction(srctext, trgtext, alignment):
    srctext = srctext.split()
    trgtext = trgtext.split()
    srclen = len(srctext)
    trglen = len(trgtext)

    e_aligned = [i for i,_ in alignment]
    f_aligned = [j for _,j in alignment]

    for e_start in range(srclen):
        for e_end in range(e_start, srclen):
            f_start, f_end = trglen-1 , -1
            for e,f in alignment:
                if e_start <= e <= e_end:
                    f_start = min(f, f_start)
                    f_end = max(f, f_end)

            if f_end < 0:
                break

            for e,f in alignment:
                if ((f_start <= f <= f_end) and (e < e_start or e > e_end)):
                    break

            fs = f_start
            while True:
                fe = f_end
                while True:
                    src_phrase = " ".join(srctext[i] for i in range(e_start, e_end+1))
                    trg_phrase = " ".join(trgtext[i] for i in range(fs, fe+1))
                    yield (src_phrase, trg_phrase)

                    fe += 1
                    if fe in f_aligned or fe == trglen:
                        break
                fs -=1 
                if fs in f_aligned or fs < 0:
                    break


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

    with codecs.open(output_file, 'w', 'utf-8') as out:
        for x, y, z in zip(sources, targets, alignments):
            for a, b in phrase_extraction(x, y, z):
                a, b = whitespace_tokenizer(a), whitespace_tokenizer(b)
                if 1 <= len(a) <= max_ngram and 1 <= len(b) <= max_ngram:
                    out.write('{0} ||| {1}\n'.format(' '.join(a), ' '.join(b)))

    logging.info((output_file))

if __name__ == '__main__':
    plac.call(main)
