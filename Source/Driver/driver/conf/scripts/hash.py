import hashlib


def get_hash(url: str) -> str:
    hash_obj = hashlib.sha256(bytes(url, 'utf-8'))
    return hash_obj.hexdigest()
