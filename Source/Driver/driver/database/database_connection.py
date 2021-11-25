import os
import psycopg2

from typing import Dict

import settings
import log


class DatabaseConnection:
    _instance = None
    _connection = None
    _cursor = None
    __database_params: Dict = None
    __db = None

    def __new__(cls, tables: str):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)

        if not cls._connection:
            try:
                cls.__set_database_params()
                cls._connection = psycopg2.connect(**cls.__database_params)
                cls._cursor = cls._connection.cursor()
                log.info("DATABASE", "Connection succeeded",
                         fore=log.Fore.LIGHTGREEN_EX)

                cls.__set_database_tables(tables)
            except Exception as e:
                log.error("DATABASE", "Connection was refused __> " + str(e))
                choice = input(
                    f"Database session is exist (on {settings.DATABASE_SESSION}), maybe was corrupted. Do you want to delete it? [y/N]") or 'N'

                if choice in ['y', 'Y']:
                    cls.reset()
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
    def __create_log(cls, params: Dict):
        try:
            with open(settings.DATABASE_SESSION, 'w') as l:
                l.write(str(params))
        except Exception as e:
            log.error("DATABASE", str(e))

    @classmethod
    def __set_database_params(cls):
        params = {}
        if os.path.exists(settings.DATABASE_SESSION):
            with open(settings.DATABASE_SESSION, 'r') as l:
                import ast
                params = ast.literal_eval(str(l.read()))

        if not params and not cls.__database_params:
            dbname = str(input("Enter dbname (postgres):") or 'postgres')
            port = int(input("Enter port (5432):") or 5432)
            user = str(input("Enter user (postgres):") or 'postgres')

            while True:
                try:
                    password = int(input("Enter password:"))
                    break
                except ValueError:
                    continue

            params = {"dbname": dbname,
                      "port": port,
                      "user": user,
                      "password": password}

            cls.__create_log(params)

        cls.__database_params = params

    @classmethod
    def __set_database_tables(cls, tables: str):
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
    def reset(cls) -> None:
        try:
            os.remove(settings.DATABASE_SESSION)
            log.info("DATABASE", "Database session is deleted",
                     fore=log.Fore.LIGHTGREEN_EX)
        except Exception as e:
            log.error("DATABASE", "Database session is not deleted __> " + str(e))

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
