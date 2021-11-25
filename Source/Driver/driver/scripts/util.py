import hashlib
import datetime

import settings

from typing import List


def get_hash(url: str) -> str:
    hash_obj = hashlib.sha256(bytes(url, 'utf-8'))
    return hash_obj.hexdigest()


def now(no_str: bool = False):
    n = datetime.datetime.now()
    if not no_str:
        return n.strftime('%Y-%m-%d %H:%M:%S')

    return n


def get_urls(urls_path: str) -> List[str]:
    with open(urls_path, 'r') as file:
        return file.read().strip().split()
