from abc import ABC
from datetime import datetime

import json
import os
import shutil
import log
import threading
import urllib
import re
import glob
import settings

from scripts import util

from webdriver.webdriver_connection import WebDriverConnection
from database.database_connection import DatabaseConnection

from scripts import parser
from database import insertions


class Cache(ABC):
    @staticmethod
    def clear(path):
        if os.path.exists(path):
            try:
                shutil.rmtree(path)
                log.info("HANDLER", f"{path} removed")
            except Exception as e:
                log.error("HANDLER", f"{path} not removed ", str(e))
                return
        else:
            log.info("HANDLER", f"{path} is already removed")

    @staticmethod
    def init(path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
                log.info("HANDLER", f"{path} is initialized")
            except Exception as e:
                log.error(
                    "HANDLER", f"{path} is not initialized ==> " + str(e))
                return
        else:
            log.info("HANDLER", f"{path} is already initialized")

    @staticmethod
    def clearAll(paths: list[str]):
        for path in paths:
            Cache.clear(path)

    @staticmethod
    def initAll(paths: list[str]):
        for path in paths:
            Cache.init(path)

    @staticmethod
    def resetAll():
        caches = [
            settings.FETCHED_CACHE,
            settings.PARSED_CACHE,
            settings.SERVER_CACHE
        ]

        Cache.clearAll(caches)
        Cache.initAll(caches)

    @staticmethod
    def writeTo(content: str, *, file: str, to: str, format: str = None, encoding: str = "utf8"):
        hashval = util.get_hash(file)
        finalpath = to + hashval

        if format:
            finalpath += f'.{format}'

        try:
            with open(finalpath, 'w+', encoding=encoding) as buffer:
                if to == settings.FETCHED_CACHE:
                    buffer.write(util.now() + '\n' + content)
                elif to == settings.PARSED_CACHE:
                    json.dump(content, buffer, indent=4, ensure_ascii=False)
                else:
                    buffer.write(content)
        except Exception as e:
            log.error("HANDLER", str(e))
            return False, str(e)

        return True, None

    @staticmethod
    def isCached(file: str, from_: str):
        hashval = util.get_hash(file)
        finalpath = from_ + hashval

        if not os.path.exists(finalpath):
            return False, None

        try:
            with open(finalpath, 'r') as buffer:
                if from_ == settings.FETCHED_CACHE:
                    date = str(buffer.readline()).strip()
                    if Cache.isExpired(date):
                        return False, None
        except Exception as e:
            log.error("HANDLER", str(e))
            return None, str(e)

        return True, None

    @staticmethod
    def readFrom(file: str, from_: str):
        hashval = util.get_hash(file)
        finalpath = from_ + hashval

        try:
            with open(finalpath, 'r') as buffer:
                content = buffer.read()
        except Exception as e:
            log.error("HANDLER", str(e))
            return False, f"{file} doesn't exist"

        return True, content

    @staticmethod
    def isExpired(date: str):
        return abs(util.now(no_str=True) - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")).days != 0


class Scheduler(ABC):
    @staticmethod
    def run(func, sec: int = 86400):
        def target():
            while not stopped.wait(sec):
                func()

        stopped = threading.Event()
        threading.Thread(target=target).start()


class Handler(ABC):

    @staticmethod
    def fetch(urls: list[str]):
        for url in urls:
            isCached, err = Cache.isCached(url, settings.FETCHED_CACHE)

            if err:
                return (500, err)

            if not isCached:
                try:
                    log.info("HANDLER", f"{url} is fetching")
                    WebDriverConnection.driver.get(url)
                    content = WebDriverConnection.driver.page_source

                    wrto, err = Cache.writeTo(content, file=url,
                                              to=settings.FETCHED_CACHE)
                    if not wrto:
                        return (400, err)

                except Exception as e:
                    log.error("HANDLER", str(e))
                    return (500, str(e))
            else:
                log.info("HANDLER", f"{url} is already in cache")
                return (200, {'already-cached': True})

        return (200, True)

    @staticmethod
    def parse(urls: list[str]):
        workers = []

        for url in urls:
            status, content = Cache.readFrom(url, settings.FETCHED_CACHE)

            if not status:
                return 500, content

            try:
                tid = threading.Thread(
                    target=parser.run, args=(url, content, Cache.writeTo, url, settings.PARSED_CACHE))
                workers.append(tid)
                tid.start()
            except Exception as e:
                log.error("HANDLER", str(e))
                return 500, str(e)

        for tid in workers:
            tid.join()

        return 200, True

    @staticmethod
    def insert(urls: list[str]):
        hashed_urls = [util.get_hash(url) for url in urls]
        products = glob.glob(settings.PARSED_CACHE + "*.json")

        for product in products:
            content_file = product.split(settings.PARSED_CACHE)[
                1].split('.json')[0]

            if content_file not in hashed_urls:
                continue

            try:
                with open(product, "r") as other:
                    insertions.insert(json.load(other))
            except Exception as e:
                log.error(content_file, str(e))
                return 500, str(e)

            log.info(content_file, "Added to database",
                     fore=log.Fore.LIGHTGREEN_EX)

        return 200, True

    @staticmethod
    def pattern_match(url: str):
        pattern = r"^(http[s]?:\/\/)?(www\.)?(hepsiburada.com\/)(\S*)$"

        return re.match(pattern, url)

    @staticmethod
    def refresh():
        try:
            DatabaseConnection.cursor.execute("""
                select url from product
            """)

            urls = DatabaseConnection.cursor.fetchall()
            urls = [url[0] for url in urls]

            if urls:
                log.info("HANDLER", "Database is refreshing")
                Cache.resetAll()

                return Handler.ordinal(urls)

            else:
                log.info("HANDLER", "Database is empty")
                return 200, "database is empty"

        except Exception as e:
            log.error("HANDLER", str(e))
            return 500, str(e)

    @staticmethod
    def track(params):
        urls = list(
            filter(lambda url: Handler.pattern_match(url), params['urls']))

        return Handler.ordinal(urls)

    @staticmethod
    def ordinal(urls: list[str]):
        errorWhen = [400, 500]

        code, msg = Handler.fetch(urls)
        if code in errorWhen:
            return code, msg

        code, msg = Handler.parse(urls)
        if code in errorWhen:
            return code, msg

        code, msg = Handler.insert(urls)
        if code in errorWhen:
            return code, msg

        return 200, True
