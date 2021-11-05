from err import TableNotCreatedError
from colorama import Fore, Style

import os
import sys
import dotenv


DOTENV_PATH = sys.path[0] + '/config/.env'


if __name__ == '__main__':
    dotenv.load_dotenv(DOTENV_PATH)
    import database as db

    for table in list(db.TABLES.STATIC_TABLES.keys()):
        try:
            if not db.QUERIES.TableIsExists(table):
                db.QUERIES.CreateNewTable(db.TABLES.STATIC_TABLES[table])
                print(Fore.GREEN + "[CREATED] " + Style.RESET_ALL + table)
            else:
                print(Fore.YELLOW + "[EXISTS] " + Style.RESET_ALL + table)

        except TableNotCreatedError:
            print(Fore.RED + "[NOT CREATED] " + Style.RESET_ALL + table)
