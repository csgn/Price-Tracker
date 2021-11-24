from conf.database.db import DatabaseConnection


def TableIsExists(table: str):
    DatabaseConnection.cursor.execute(f"""
        select exists(select relname from pg_class
            where relname='{table.lower()}')
    """)

    return DatabaseConnection.cursor.fetchone()[0]


def CreateNewTable(schema: str):
    DatabaseConnection.cursor.execute(schema)
    DatabaseConnection.connection.commit()
