import sys
import dotenv
import threading
import json
import glob

from colorama import Fore
from bs4 import BeautifulSoup

import fetch

from parser import *
from debug import ERROR, INFO

DOTENV_PATH = sys.path[0] + '/config/.env'
PRODUCTS_FOLDER = "./.products/"


def parse(url: str, content: str):
    url_hash = fetch.get_hash(url)
    parser = BeautifulSoup(content, "lxml")

    INFO(url_hash, "is being parsed")

    product_name = PARSE__PRODUCT_NAME(parser)
    brand = PARSE__PRODUCT_BRAND(parser)
    price = PARSE__PRODUCT_PRICE(parser)
    rate = PARSE__PRODUCT_RATE(parser)
    images = PARSE__PRODUCT_IMAGES(parser)
    supplier = PARSE__PRODUCT_SUPPLIER(parser)
    category = PARSE__PRODUCT_CATEGORY(parser)
    subcategory = PARSE__PRODUCT_SUBCATEGORY(parser)

    resval = {
        "product name": product_name,
        "url": url,
        "brand": brand,
        "price": " ".join(price),
        "rate": rate,
        "images": images,
        "supplier": supplier,
        "category": category,
        "subcategory": subcategory,
    }

    with open(PRODUCTS_FOLDER + url_hash + '.json', "w+", encoding='utf8') as file:
        json.dump(resval, file, indent=4, ensure_ascii=False)


def insert(product_file):
    with open(product_file, "r") as fp:
        product_json = json.load(fp)
        db.insertions.insert_to_db(product_json)


def get_urls():
    with open('./config/URLs', 'r') as file:
        return file.read().split()


if __name__ == '__main__':
    """ SET DATABASE CONFIG """
    dotenv.load_dotenv(DOTENV_PATH)
    import database as db

    """ CREATE TABLE IF NOT EXISTS """
    for table, query in list(db.tables.STATIC_TABLES.items()):
        try:
            if not db.queries.TableIsExists(table):
                db.queries.CreateNewTable(query)
                INFO(table, "is being created")
            else:
                INFO(table, "already exists", tc=Fore.MAGENTA)

        except Exception as e:
            ERROR(e.__str__())
            INFO(table, "not created", tc=Fore.RED)

    """ FETCH CONTENT FROM URL/CACHE and PARSE CONTENT to JSON """
    workers = []
    urls = get_urls()

    for url in urls:
        content = fetch.get_content(url)
        tid = threading.Thread(target=parse, args=(url, content,))
        workers.append(tid)
        tid.start()

    for tid in workers:
        fetch.driver.quit()
        tid.join()

    """ INSERT TO DATABASE from JSON FILE """
    products = glob.glob(PRODUCTS_FOLDER + "*.json")
    for product in products:
        INFO(product.split(PRODUCTS_FOLDER)[1].split(
            '.json')[0], "is being inserted to database")
        insert(product)

    db.cursor.close()
    db.connection.close()
