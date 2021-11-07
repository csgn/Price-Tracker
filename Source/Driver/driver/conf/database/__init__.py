from . import insertions, queries, tables, schemas

import os
import psycopg2 as ps2

connection = ps2.connect(os.environ["DATABASE_URI"])
cursor = connection.cursor()
