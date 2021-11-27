import os
import json
import glob
import threading
import shutil

from urllib.parse import urlparse
from datetime import datetime

from http.server import SimpleHTTPRequestHandler, HTTPServer
from webdriver.webdriver_connection import WebDriverConnection
from database.database_connection import DatabaseConnection
from database import insertions

import log
import settings
from scripts import util, parser


class DriverServerHandler(SimpleHTTPRequestHandler):
    caches = [settings.SERVER_CACHE,
              settings.PARSER_CACHE, settings.URLS_CACHE]

    @classmethod
    def run_forever(cls, port: int, handler: SimpleHTTPRequestHandler, tables: str):
        cls.create_caches()

        dconn = DatabaseConnection(tables)
        wconn = WebDriverConnection()

        try:
            log.info(
                "SERVER", f"http://localhost:{port} is listening...")
            httpserver = HTTPServer(('localhost', port), handler)
            cls.set_scheduler()
            httpserver.serve_forever()
        except Exception as e:
            log.error("SERVER", "Server Handler was refused __> " + str(e))

        dconn.close()
        wconn.close()

    @classmethod
    def create_caches(cls):
        if not os.path.exists(settings.CACHE_FOLDER):
            os.makedirs(settings.CACHE_FOLDER)

        for cache in cls.caches[:-1]:
            if not os.path.exists(cache):
                log.info("SERVER", f"{cache} is created",
                         fore=log.Fore.LIGHTGREEN_EX)
                os.makedirs(cache)
            else:
                log.info("SERVER", f"{cache} was already created")

        if not os.path.exists(cls.caches[-1]):
            try:
                open(settings.URLS_CACHE, 'a').close()
                log.info("SERVER", f"{cls.caches[-1]} is created")
            except Exception as e:
                log.error("SERVER", str(e))
        else:
            log.info("SERVER", f"{cls.caches[-1]} was already created")

    @classmethod
    def clear_caches(cls):
        for cache in cls.caches[:-1]:
            if os.path.exists(cache):
                try:
                    shutil.rmtree(cache)
                    log.info("SERVER", f"{cache} is cleaned",
                             fore=log.Fore.LIGHTGREEN_EX)
                except Exception as e:
                    log.error("SERVER", str(e))
            else:
                log.info("SERVER", f"{cache} was already cleaned")

        if os.path.exists(cls.caches[-1]):
            try:
                os.remove(cls.caches[-1])
                log.info("SERVER", f"{cls.caches[-1]} is cleaned")
            except Exception as e:
                log.error("SERVER", str(e))
        else:
            log.info("SERVER", f"{cache} was already cleaned")

    @classmethod
    def set_scheduler(cls):
        stopped = threading.Event()

        def refresh():
            # every 24 hours
            while not stopped.wait(86400):
                cls.refresh()

        threading.Thread(target=refresh).start()

        return stopped.set

    @classmethod
    def body_parser(cls, post_data: str) -> dict:
        try:
            return json.loads(str(post_data, "utf-8"))
        except Exception as e:
            log.error("SERVER", "Parsing error __> " + str(e))

    @classmethod
    def is_cached(cls, url: str) -> bool:
        maybe_cached = cls.read_one(url)

        if maybe_cached:
            if os.path.exists(settings.SERVER_CACHE + util.get_hash(url)):
                date = maybe_cached.split(',')[0]
                if abs(util.now(no_str=True) - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")).days == 0:
                    log.info("SERVER", f"{url} already cached")
                    return True

        log.info("SERVER", f"{url} is being cached")
        cls.add_cache([url, ])

        return False

    @classmethod
    def insert(cls, urls: list[str]):
        """ INSERT TO DATABASE from JSON FILE """

        hashed_urls = [util.get_hash(url) for url in urls]
        products = glob.glob(settings.PARSER_CACHE + "*.json")
        for product in products:
            content_file = product.split(settings.PARSER_CACHE)[
                1].split('.json')[0]

            if content_file not in hashed_urls:
                continue

            log.info(content_file, "is being inserted to database")
            try:
                with open(product, "r") as other:
                    insertions.insert(json.load(other))

                log.info(content_file, "was inserted to database",
                         fore=log.Fore.LIGHTGREEN_EX)
            except Exception as e:
                log.error(content_file, str(e))

    @classmethod
    def fetch(cls, urls: list[str]):
        for url in urls:
            if not cls.is_cached(url):
                try:
                    log.info("SERVER", f"{url} fetching...")
                    WebDriverConnection.driver.get("https://"+url)
                    content = WebDriverConnection.driver.page_source

                    with open(settings.SERVER_CACHE + util.get_hash(url.strip()), 'w+') as file:
                        file.write(content)
                        log.info("SERVER", url.strip() + ' is saved')
                except Exception as e:
                    log.error("SERVER", str(e))

    @classmethod
    def parse(cls, urls: list[str]):
        workers = []

        for url in urls:
            with open(settings.SERVER_CACHE + util.get_hash(url), "r") as file:
                content = file.read()

            tid = threading.Thread(
                target=parser.run, args=(url, content,))
            workers.append(tid)
            tid.start()

        for tid in workers:
            tid.join()

    @classmethod
    def refresh(cls):
        try:
            DatabaseConnection.cursor.execute("""
                select url from product;
            """)
            urls = DatabaseConnection.cursor.fetchall()
            urls = [url[0] for url in urls]
            log.info("SERVER", "URLs is fetched from database")

            if urls:
                log.info("SERVER", "URLs is being refreshed")
                cls.clear_caches()
                cls.create_caches()
                cls.fetch(urls)
                cls.parse(urls)
                cls.insert(urls)
            else:
                log.info("SERVER", "Database is empty")

        except Exception as e:
            log.error("SERVER", str(e))

    @classmethod
    def read_one(cls, url: str):
        lines = cls.read_cache()

        for line in lines:
            if line and line.split(',')[1] == url:
                return line

    @classmethod
    def read_cache(cls):
        with open(settings.URLS_CACHE, "r") as f:
            lines = f.read().strip().split('\n')

        return lines

    @classmethod
    def add_cache(cls, urls: list[str]):
        lines = cls.read_cache()

        with open(settings.URLS_CACHE, "w") as f:
            for line in lines:
                if line:
                    url = line.split(',')[1]
                    if url not in urls:
                        f.write(line + '\n')

            for url in urls:
                f.write(f"{util.now()},{cls.url_parse(url)}\n")

    @classmethod
    def url_parse(cls, url: str):
        url = urlparse(url)
        return url.netloc + url.path

    @classmethod
    def tracking(cls, params: list[str]):
        if params:
            urls = [cls.url_parse(url) for url in params]
            cls.fetch(urls)
            cls.parse(urls)
            cls.insert(urls)

    def do_GET(self):
        if self.path == '/refresh':
            try:
                self.refresh()
                self.send_response(200)
            except:
                self.send_response(500)
        else:
            self.send_response(404)

        self.end_headers()

    def do_POST(self):
        if self.path == '/track':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)

                params = list(set(self.body_parser(post_data)['urls']))
                self.tracking(params)
                self.send_response(200)
            except:
                self.send_response(500)
        else:
            self.send_response(404)

        self.end_headers()

    def do_OPTIONS(self):
        if self.path == '/track':
            self.send_response(200)
        else:
            self.send_response(404)

        self.end_headers()

    def end_headers(self) -> None:
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.send_header(
            'Access-Control-Allow-Methods', 'GET, POST')
        self.send_header(
            'Access-Control-Allow-Headers', 'Origin, Content-Type, X-Auth-Token')
        SimpleHTTPRequestHandler.end_headers(self)
