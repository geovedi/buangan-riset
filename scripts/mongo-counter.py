# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
logging.basicConfig(format='%(asctime)s [%(process)d] [%(levelname)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

from smart_open import smart_open
from glob import glob
from concurrent import futures

import pymongo

conn = pymongo.MongoClient()
db = conn.db
collection = db.collection

collection.create_index('s', background=True)

def counter(fname):
    for line_no, line in enumerate(smart_open(fname)):
        collection.update(
            {'s': line = line.decode('utf-8').lower().strip()},
            {'$inc': {'c': 1}},
            upsert=True
        )
        if line_no % 10000 == 0:
            logging.info((fname, line_no, line))

with futures.ProcessPoolExecutor() as executor:
    executor.map(counter, glob('phrases/*.gz'))
