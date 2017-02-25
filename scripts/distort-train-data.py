# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io
import plac
import numpy as np

import logging
logging.basicConfig(
    format='%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

def main(input_fname, output_fname):
    with io.open(output_fname, 'w', encoding='utf-8') as out:
        for line_no, line in enumerate(io.open(input_fname, 'r', encoding='utf-8')):
            parts = line.strip().split(' ||| ')

            if len(parts) != 2:
                continue

            src, tgt = parts
            src_tok = src.split()
            src_len = len(src_tok)

            # 1. always add the original pair
            out.write('{} ||| {}\n'.format(src, tgt))

            # 2. distort src but keep tgt
            for p in [0.1, 0.2, 0.3]:
                dist_src_tok = src_tok

                for i in np.random.randint(src_len, size=int(src_len * p)):
                    dist_src_tok[i] = '<unk>'
                out.write('{} ||| {}\n'.format(' '.join(dist_src_tok), tgt))

            if line_no % 10000 == 0:
                logging.info('processing pair: {}'.format(line_no))


if __name__ == '__main__':
    plac.call(main)


