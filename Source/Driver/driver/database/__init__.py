import os
import sys
import psycopg2 as ps2

from colorama import Style, Fore

from . import (
    schemas as SCHEMAS,
    insertions as INSERTIONS,
    queries as QUERIES,
    tables as TABLES
)

connection = ps2.connect(os.environ["DATABASE_URI"])
cursor = connection.cursor()
