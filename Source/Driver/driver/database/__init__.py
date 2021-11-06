import os
import psycopg2 as ps2
from psycopg2 import pool


from . import insertions, tables, schemas, tables, queries

connection = ps2.connect(os.environ["DATABASE_URI"])
cursor = connection.cursor()
