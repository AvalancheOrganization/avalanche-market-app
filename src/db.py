import os

from deta import Deta
from tqdm import tqdm

DETA_BLOCK_SIZE = 25
DETA_PROJECT_KEY = os.getenv("DETA_PROJECT_KEY")


def get_db(name):
    return Deta(DETA_PROJECT_KEY).Base(name)


def fetch_db(db_name, query=None):
    print(f" # [Data] fetching {db_name}, {query}...")
    db = get_db(db_name)
    resp = db.fetch(query=query)
    items = resp.items
    while resp.last:
        resp = db.fetch(query=query, last=resp.last)
        items += resp.items

    print(f" # [Data] Got {len(items)} items")
    return items


def put_chunks_db(db_name, rows):
    print(f" # [Data] writing data in {db_name} ...")
    db = get_db(db_name)
    n_chunks = len(rows) // DETA_BLOCK_SIZE + 1
    for idx_chunk in tqdm(range(n_chunks)):
        start = idx_chunk * DETA_BLOCK_SIZE
        end = (idx_chunk + 1) * DETA_BLOCK_SIZE
        data_chunk = rows[start:end]
        db.put_many(data_chunk)


def update_db(db_name, keys, customers):
    print(f" # [Data] updating {db_name} ...")
    db = get_db(db_name)
    for key, customer in tqdm(zip(keys, customers)):
        row = customer.dict()
        db.update(row, key)
