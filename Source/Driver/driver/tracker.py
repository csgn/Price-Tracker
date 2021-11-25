import os
import click

import settings

from handler.server_handler import DriverServerHandler
from webdriver.webdriver_connection import WebDriverConnection
from database.database_connection import DatabaseConnection


@click.group()
def cli():
    pass


@click.command()
@click.option('--port', type=int, default=4444)
@click.option('--tables', type=str)
def runserver(port: int, tables: str):
    dconn = DatabaseConnection(tables)
    wconn = WebDriverConnection()

    DriverServerHandler.run_forever(port, DriverServerHandler)

    DatabaseConnection.close()
    WebDriverConnection.close()


if __name__ == '__main__':
    if not os.path.exists(settings.CACHE_FOLDER):
        os.makedirs(settings.CACHE_FOLDER)

    if not os.path.exists(settings.SERVER_CACHE):
        os.makedirs(settings.SERVER_CACHE)

    if not os.path.exists(settings.PARSER_CACHE):
        os.makedirs(settings.PARSER_CACHE)

    cli.add_command(runserver)
    cli()
