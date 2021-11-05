import database as db


def TableIsExists(table: str):
    db.cursor.execute(f"""
        select exists(select relname from pg_class
                where relname='{table.lower()}')
    """)

    return db.cursor.fetchone()[0]


def CreateNewTable(schema: str):
    db.cursor.execute(schema)
    db.connection.commit()
