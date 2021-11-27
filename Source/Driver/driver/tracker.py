import click


from handler.server_handler import DriverServerHandler
from webdriver.webdriver_connection import WebDriverConnection
from database.database_connection import DatabaseConnection


@click.group()
def cli():
    pass


@click.command()
@click.option('--tables', type=str)
def runserver(tables: str):
    DriverServerHandler.run_forever(4444, DriverServerHandler, tables)


@click.command()
def clearcache():
    DriverServerHandler.clear_caches()


if __name__ == '__main__':
    cli.add_command(runserver)
    cli.add_command(clearcache)
    cli()
