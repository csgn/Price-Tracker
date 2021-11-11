import hashlib
import datetime
import conf.global_settings as settings


def get_hash(url: str) -> str:
    hash_obj = hashlib.sha256(bytes(url, 'utf-8'))
    return hash_obj.hexdigest()


def now():
    n = datetime.datetime.now()
    return n.strftime('%Y-%m-%d %H:%M:%S')


def get_urls():
    with open(settings.URLS_FOLDER, 'r') as file:
        return file.read().split()
