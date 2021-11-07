from contextlib import AbstractContextManager
import conf.database as db


class AlterCursor(AbstractContextManager):
    def __init__(self):
        self.__cursor = None

    def __enter__(self):
        self.__cursor = db.connection.cursor()
        return self

    def __exit__(self, *args):
        self.__cursor.close()

    def fetch(self):
        res = self.__cursor.fetchone()
        return res if res is None else res[0]

    @property
    def cursor(self):
        return self.__cursor
