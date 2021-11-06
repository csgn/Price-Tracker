import os
import sys
import dotenv
import threading
import pprint
import json

from colorama import Fore, Style
from bs4 import BeautifulSoup
from tqdm import tqdm

import fetch
from parser import *
from err import TableNotCreatedError

DOTENV_PATH = sys.path[0] + '/config/.env'

PRODUCTS_FOLDER = "./.products/"

def worker(url: str):
    content = fetch.get_content(url)
    url_hash = fetch.get_hash(url)

    parser = BeautifulSoup(content, "lxml")

    print(Fore.YELLOW + "[INFO] " + Style.RESET_ALL + Fore.GREEN + url_hash + Style.RESET_ALL + " is being parsed")
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


def get_urls():
    with open('./config/URLs', 'r') as file:
        return file.read().split()

if __name__ == '__main__':
    dotenv.load_dotenv(DOTENV_PATH)
    import database as db

    for table in list(db.TABLES.STATIC_TABLES.keys()):
        try:
            if not db.QUERIES.TableIsExists(table):
                db.QUERIES.CreateNewTable(db.TABLES.STATIC_TABLES[table])
                print(Fore.YELLOW + "[INFO] " + Style.RESET_ALL + Fore.GREEN + table + Style.RESET_ALL + " is being created")
            else:
                print(Fore.YELLOW + "[INFO] " + Style.RESET_ALL + Fore.GREEN + table + Style.RESET_ALL + " already exists")

        except TableNotCreatedError:
            print(Fore.RED + "[INFO] " + Style.RESET_ALL + Fore.GREEN + table + Style.RESET_ALL + " not created")

    
    workers = []
    urls = get_urls()
    for url in tqdm(urls):
        worker(url)
        tid = threading.Thread(target=worker, args=(url,))
        workers.append(tid)
        tid.start()

    for tid in workers:
        tid.join()
        fetch.driver.quit()

    

