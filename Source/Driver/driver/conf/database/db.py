import os
import psycopg2

from abc import ABC

import conf.logger as log


class DatabaseConnection(ABC):
    connection = None
    cursor = None

    @staticmethod
    def init() -> bool:
        if DatabaseConnection.connection:
            log.info("DB", "is exists")
            return

        try:
            kwargs = {}
            if os.path.exists('.dblog'):
                with open('.dblog', 'r') as dblog:
                    import ast
                    kwargs = dblog.read()
                    kwargs = ast.literal_eval(str(kwargs))

            if not kwargs:
                dbname = input("Enter dbname(postgres):")
                port = input("Enter port(5432):")
                user = input("Enter user(postgres):")
                password = int(input("Enter password:"))

                dbname = dbname if dbname else "postgres"
                port = int(port) if port else 5432
                user = user if user else "postgres"

                kwargs = {"dbname": dbname, "port": port,
                          "user": user, "password": password}

            DatabaseConnection.connection = psycopg2.connect(**kwargs)
            DatabaseConnection.cursor = DatabaseConnection.connection.cursor()
            log.info("DB", "Connection is succesfull",
                     fore=log.Fore.LIGHTGREEN_EX)
        except Exception as e:
            log.error("DB", str(e))
            return False

        try:
            with open('.dblog', 'w') as dblog:
                dblog.write(str(kwargs))
            log.info("DB", "log created", fore=log.Fore.LIGHTGREEN_EX)
        except Exception as e:
            log.error("DB", str(e))
            return False

        return True

    @staticmethod
    def reset() -> bool:
        try:
            os.remove('.dblog')
            log.info("DB", "is reseted", fore=log.Fore.LIGHTGREEN_EX)
        except Exception as e:
            log.error("DB", str(e))
            return False

        return True

    @staticmethod
    def close() -> bool:
        DatabaseConnection.cursor.close()
        DatabaseConnection.connection.close()
