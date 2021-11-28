import os
import sys
import psycopg2

import log


class DatabaseConnection:
    _instance = None
    _connection = None
    _cursor = None

    def __new__(cls, tables: str):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)

        if not cls._connection:
            try:
                cls._connection = psycopg2.connect(
                    os.environ["DATABASE_URL"])
                cls._cursor = cls._connection.cursor()
                log.info("DATABASE", "Connection succeeded",
                         fore=log.Fore.LIGHTGREEN_EX)

                cls.create_database_tables(tables)
            except Exception as e:
                log.error("DATABASE", "Connection was refused __> " + str(e))
                sys.exit(0)
        else:
            log.error("DATABASE", "Connection was already opened")

        return cls._instance

    @classmethod
    @property
    def status(cls):
        return cls._connection is not None

    @classmethod
    @property
    def connection(cls):
        return cls._connection

    @classmethod
    @property
    def cursor(cls):
        return cls._cursor

    @classmethod
    def create_database_tables(cls, tables: str):
        """ CREATE TABLE IF NOT EXISTS """
        with open(tables, "r") as file:
            try:
                DatabaseConnection.cursor.execute(file.read())
                log.info("DRIVER", "SQL including was succeed __> " + DatabaseConnection.cursor.statusmessage,
                         fore=log.Fore.LIGHTGREEN_EX)
                DatabaseConnection.connection.commit()
            except Exception as e:
                log.error("DRIVER", "SQL including was refused __>" + str(e))

    @classmethod
    def close(cls) -> None:
        if cls._cursor:
            cls._cursor.close()
            log.info("DATABASE", "Cursor is closed")

        if cls._connection:
            cls._connection.close()
            log.info("DATABASE", "Connection is closed")

        if cls._instance:
            cls._instance = None
