from datetime import datetime


def now():
    n = datetime.now()
    return n.strftime('%Y-%m-%d %H:%M:%S')
