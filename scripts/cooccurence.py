# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import plac
import struct

import logging
logging.basicConfig(format='%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)


def main(binfile, outfile):
    line_no = 0
    with open(outfile, 'w') as out:
        with open(binfile, 'rb') as f:
            byte = f.read(16)
            while byte != b'':
                out.write('{0}\t{1}\t{2}\n'.format(*struct.unpack('<iid', byte)))
                byte = f.read(16)
                if line_no % 10000 == 0:
                    logging.info((line_no))
                line_no += 1

if __name__ == '__main__':
    plac.call(main)
