# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import fileinput
from itertools import izip

def process(block):
    # currently focus on chunk, ner, and srl
    sentence, lines = block[0], block[1:]
    offsets, ners, chunks, srls = [], [], [], []

    # token, start, end, pos, chunk, ner, srl_verb, srl_n+
    for line in lines:
        parts = line.strip().split()
        offsets.append([int(parts[1]), int(parts[2])])
        chunks.append(parts[4])
        ners.append(parts[5])
        srls.append(tuple(parts[7:]))

    srls = list(izip(*srls))

    phrases = []
    for (offset_start, offset_end), tok in zip(offsets, chunks):
        if tok == 'O': continue
        iobes, label = tok.split('-', 1)
        if iobes in ['S', 'I']: continue
        if iobes == 'B':
            phrases.append([offset_start, offset_end, label])
        elif iobes == 'E':
            try:
                phrases[-1][1] = offset_end
            except IndexError:
                pass

    for offset_start, offset_end, label in phrases:
        print('{0}\t{1}'.format(label, sentence[offset_start:offset_end]))

    phrases = []
    for (offset_start, offset_end), tok in zip(offsets, ners):
        if tok == 'O': continue
        iobes, label = tok.split('-', 1)
        if iobes in ['S', 'I']: continue
        if iobes == 'B':
            phrases.append([offset_start, offset_end, label])
        elif iobes == 'E':
            try:
                phrases[-1][1] = offset_end
            except IndexError:
                pass

    for offset_start, offset_end, label in phrases:
        print('{0}\t{1}'.format(label, sentence[offset_start:offset_end]))

    for srl in srls:
        phrases = []
        for (offset_start, offset_end), tok in zip(offsets, srl):
            if tok == 'O': continue
            iobes, label = tok.split('-', 1)
            if iobes in ['S', 'I']: continue
            if iobes == 'B':
                phrases.append([offset_start, offset_end, label])
            elif iobes == 'E':
                try:
                    phrases[-1][1] = offset_end
                except IndexError:
                    pass

        for offset_start, offset_end, label in phrases:
            print('{0}\t{1}'.format(label, sentence[offset_start:offset_end]))


def main():
    block = []
    for line in fileinput.input():
        # expected input from ```senna -offsettags -pos -chk -ner -srl```
        line = line.strip()
        if line:
            block.append(line)
        else:
            process(block)
            block = []

if __name__ == '__main__':
    main()
