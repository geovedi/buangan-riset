# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import plac
import fileinput
import logging
logging.basicConfig(format='%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def main():
    chunks = []
    previous = 'O'
    counter = 0
    for line in fileinput.input():
        line = line.encode('utf-8')
        parts = line.strip().split()
        if not parts:
            for chunk, label in chunks:
                phrase = ' '.join(chunk)
                print('{0}\t{1}'.format(label, phrase))
                if counter % 100000 == 0:
                    logging.info(counter)
                counter += 1
            chunks = []
        else:
            word, label = parts
            try:
                if label.startswith('S-') or label.startswith('B-'):
                    label = label.split('-')[1]
                    chunks.append(([word], label))
                elif label.startswith('I-') or label.startswith('E-'):
                    chunks[-1][0].append(word)
            except:
                pass

if __name__ == '__main__':
    plac.call(main)
