import os
import shutil
import sys
import threading
import json
import glob
import click

from typing import List

import conf.logger as log
import conf.global_settings as settings

from conf.database import insertions, queries, tables
from conf.scripts import parser, fetch, util
from conf.webdriver import DriverConnection
from conf.database.db import DatabaseConnection


@click.group()
def cli():
    pass


@cli.command()
@click.option('--url', help='Enter url of product', type=str)
@click.option('--url-list', help='Enter list of urls', type=str)
@click.option('--url-path', help='Enter list of url path', type=str)
def track(url: str = None, url_list: str = None, url_path: str = None):
    urls = []
    if url:
        urls.append(url)
    elif url_list:
        urls = url_list.split(',')
    elif url_path:
        urls = util.get_urls(url_path)
    else:
        log.error("CLI", "Missing Options. Try 'tracker.py track --help' for help")
        sys.exit(0)

    driver_run(urls)


@cli.command()
def refreshdb():
    clear_cache()
    initdb()

    DatabaseConnection.cursor.execute("""
        select url from product
    """)

    res = DatabaseConnection.cursor.fetchall()
    urls = [url[0] for url in res]
    driver_run(urls)


@cli.command()
def resetdb():
    DatabaseConnection.reset()


@cli.command()
def clearcache():
    clear_cache()


def clear_cache():
    if os.path.exists(settings.CACHE_FOLDER):
        shutil.rmtree(settings.CACHE_FOLDER)
        log.info("CACHE", settings.CACHE_FOLDER + " was deleted")
    else:
        log.info("CACHE", settings.CACHE_FOLDER + " is not exists")

    if os.path.exists(settings.PRODUCTS_FOLDER):
        shutil.rmtree(settings.PRODUCTS_FOLDER)
        log.info("CACHE", settings.PRODUCTS_FOLDER + " was deleted")
    else:
        log.info("CACHE", settings.PRODUCTS_FOLDER + " is not exists")


def initdb() -> None:
    if DatabaseConnection.connection is None:
        if not DatabaseConnection.init():
            sys.exit(0)


def create_tables() -> None:
    """ CREATE TABLE IF NOT EXISTS """
    for table, query in list(tables.STATIC_TABLES.items()):
        try:
            if not queries.TableIsExists(table):
                log.info(table, "is being created")
                queries.CreateNewTable(query)
            else:
                log.info(table, "is already exists",
                         fore=log.Fore.LIGHTBLUE_EX)

        except Exception as e:
            log.error(table, str(e), fore=log.Fore.LIGHTRED_EX)
            sys.exit(0)


def fetch_and_parse(urls: List[str]) -> None:
    """ FETCH CONTENT FROM URL/CACHE and PARSE CONTENT to JSON """
    workers = []

    for url in urls:
        content = fetch.run(url)
        if content:
            tid = threading.Thread(
                target=parser.run, args=(url, content,))
            workers.append(tid)
            tid.start()

    for tid in workers:
        tid.join()


def insert_to_db(urls: list[str]) -> None:
    """ INSERT TO DATABASE from JSON FILE """
    products = glob.glob(settings.PRODUCTS_FOLDER + "*.json")
    for product in products:
        content_file = product.split(settings.PRODUCTS_FOLDER)[
            1].split('.json')[0]

        log.info(content_file, "is being inserted to database")
        try:
            with open(product, "r") as other:
                insertions.insert(json.load(other))

            log.info(content_file, "was inserted to database",
                     fore=log.Fore.LIGHTGREEN_EX)
        except Exception as e:
            log.error(content_file, str(e))


def driver_run(urls: List[str]):
    DriverConnection.init()
    initdb()
    create_tables()

    if not os.path.exists(settings.CACHE_FOLDER):
        os.makedirs(settings.CACHE_FOLDER)

    if not os.path.exists(settings.PRODUCTS_FOLDER):
        os.makedirs(settings.PRODUCTS_FOLDER)

    fetch_and_parse(urls)
    insert_to_db(urls)

    DatabaseConnection.close()
    DriverConnection.driver.quit()


if __name__ == '__main__':
    cli.add_command(track)
    cli.add_command(refreshdb)
    cli.add_command(resetdb)
    cli.add_command(clearcache)
    cli()
