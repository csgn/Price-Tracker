import os
import shutil
import sys
import threading
import json
import glob
import click

import log
import settings

from scripts import parser, fetch, util
from database import insertions

from webdriver.webdriver_connection import WebDriverConnection
from database.database_connection import DatabaseConnection


@click.group()
def cli():
    pass


@cli.command()
@click.option('--url', help='Enter a url of product', type=str)
@click.option('--path', help='Enter list of url path', type=str)
@click.option('--db', help="Enter a sql file path", type=str, required=True)
def track(url: str = None, path: str = None, db: str = None):
    if not url and not path:
        log.error(
            "DRIVER", "Missing option Try 'tracker.py track --help' for help.")
        sys.exit(0)

    if not DatabaseConnection.status:
        dconn = DatabaseConnection()

    create_tables(db)

    if not WebDriverConnection.status:
        wconn = WebDriverConnection()

    urls = []
    if url:
        urls.append(url)
        driver_run(urls)
    elif path:
        urls = util.get_urls(path)
        driver_run(urls, thread=True)


def create_tables(db: str) -> None:
    """ CREATE TABLE IF NOT EXISTS """
    with open(db, "r") as file:
        try:
            DatabaseConnection.cursor.execute(file.read())
            log.info("DRIVER", "SQL including was succeed __> " + DatabaseConnection.cursor.statusmessage,
                     fore=log.Fore.LIGHTGREEN_EX)
            DatabaseConnection.connection.commit()
        except Exception as e:
            log.error("DRIVER", "SQL including was refused __>" + str(e))
            sys.exit(0)


def fetch_and_parse(urls: list[str], thread: bool = False) -> None:
    """ FETCH CONTENT FROM URL/CACHE and PARSE CONTENT to JSON """

    workers = []

    for url in urls:
        content = fetch.run(url)

        if content:
            if thread:
                tid = threading.Thread(
                    target=parser.run, args=(url, content,))
                workers.append(tid)
                tid.start()
            else:
                parser.run(url, content)

    for tid in workers:
        tid.join()


def insert_to_db(urls: list[str]) -> None:
    """ INSERT TO DATABASE from JSON FILE """
    products = glob.glob(settings.PARSER_CACHE + "*.json")
    for product in products:
        content_file = product.split(settings.PARSER_CACHE)[
            1].split('.json')[0]

        log.info(content_file, "is being inserted to database")
        try:
            with open(product, "r") as other:
                insertions.insert(json.load(other))

            log.info(content_file, "was inserted to database",
                     fore=log.Fore.LIGHTGREEN_EX)
        except Exception as e:
            log.error(content_file, str(e))


def driver_run(urls: list[str], *, thread: bool = False):
    fetch_and_parse(urls, thread)
    insert_to_db(urls)

    DatabaseConnection.close()


if __name__ == '__main__':
    if not os.path.exists(settings.CACHE_FOLDER):
        os.makedirs(settings.CACHE_FOLDER)

    if not os.path.exists(settings.WEBDRIVER_CACHE):
        os.makedirs(settings.WEBDRIVER_CACHE)

    if not os.path.exists(settings.PARSER_CACHE):
        os.makedirs(settings.PARSER_CACHE)

    cli.add_command(track)
    cli()
