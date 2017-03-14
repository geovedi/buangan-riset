# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import io
import multivec
import fire
import numpy as np

import logging
logging.basicConfig(
    format='%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)


def main(multivec_model, source, target, output):
    model = multivec.BilingualModel(multivec_model.encode('utf-8'))

    with io.open(output, 'w', buffering=1, encoding='utf-8') as out:
        with io.open(source, 'r', encoding='utf-8') as source_f, \
             io.open(target, 'r', encoding='utf-8') as target_f:
             for i, (src, tgt) in enumerate(zip(source_f, target_f)):
                src = src.strip().encode('utf-8')
                tgt = tgt.strip().encode('utf-8')
                dist = model.similarity_bag_of_words(src, tgt)
                dist = np.clip(dist, 0.0, 1.0)
                out.write('{0:04f}\n'.format(dist))
                if i % 10000 == 0:
                    logging.info('progress: #{0}'.format(i))

if __name__ == '__main__':
    fire.Fire(main)
