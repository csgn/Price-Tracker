import threading
import json
import glob

import conf.global_settings as settings
import conf.database as db
import conf.webdriver as driver
import conf.scripts.fetch as fetch
import conf.scripts.parser as parse
import conf.logger as log


def get_urls():
    with open(settings.URLS_FOLDER, 'r') as file:
        return file.read().split()


def main():
    """ CREATE TABLE IF NOT EXISTS """
    for table, query in list(db.tables.STATIC_TABLES.items()):
        try:
            if not db.queries.TableIsExists(table):
                log.info(table, "is being created")
                db.queries.CreateNewTable(query)
            else:
                log.info(table, "is already exists")

        except Exception as e:
            log.error(table, "is not created")

    """ FETCH CONTENT FROM URL/CACHE and PARSE CONTENT to JSON """
    workers = []
    urls = get_urls()

    for url in urls:
        content = fetch.get(url)
        if content:
            tid = threading.Thread(target=parse.parse, args=(url, content,))
            workers.append(tid)
            tid.start()

    for tid in workers:
        tid.join()

    """ INSERT TO DATABASE from JSON FILE """
    products = glob.glob(settings.PRODUCTS_FOLDER + "*.json")
    for product in products:
        content_file = product.split(settings.PRODUCTS_FOLDER)[
            1].split('.json')[0]

        log.info(content_file, "is being inserted to database")
        try:
            with open(product, "r") as other:
                db.insertions.insert(json.load(other))

            log.info(content_file, "is inserted to database")
        except Exception as e:
            print(e)
            log.error(content_file, "is not inserted to database")

    driver.driver.quit()
    db.cursor.close()
    db.connection.close()
