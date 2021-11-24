import hashlib
import datetime
import conf.global_settings as settings

from typing import List


def get_hash(url: str) -> str:
    hash_obj = hashlib.sha256(bytes(url, 'utf-8'))
    return hash_obj.hexdigest()


def now():
    n = datetime.datetime.now()
    return n.strftime('%Y-%m-%d %H:%M:%S')


def get_urls(urls_path: str) -> List[str]:
    with open(urls_path, 'r') as file:
        return file.read().strip().split()
