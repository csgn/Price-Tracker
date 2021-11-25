import os
import json
import threading
import glob

from urllib.parse import urlparse
from datetime import datetime

from http.server import BaseHTTPRequestHandler, HTTPServer
from webdriver.webdriver_connection import WebDriverConnection
from database.database_connection import DatabaseConnection
from database import insertions

import log
import settings
from scripts import util, parser


class DriverServerHandler(BaseHTTPRequestHandler):
    @staticmethod
    def run_forever(port: int, handler: BaseHTTPRequestHandler):
        try:
            log.info(
                "DRIVER", f"http://localhost:{port} is listening...")
            httpserver = HTTPServer(('localhost', port), handler)
            httpserver.serve_forever()
        except Exception as e:
            log.error("DRIVER", "Server Handler was refused __> " + str(e))

    def body_parser(self, post_data: str) -> dict:
        try:
            return json.loads(str(post_data, "utf-8"))
        except Exception as e:
            log.error("SERVER", "Parsing error __> " + str(e))

    def is_cached(self, url: str) -> bool:
        maybe_cached = self.read_one(url)

        if maybe_cached:
            if os.path.exists(settings.SERVER_CACHE + util.get_hash(url)):
                date = maybe_cached.split(',')[0]
                if abs(util.now(no_str=True) - datetime.strptime(date, "%Y-%m-%d %H:%M:%S")).days == 0:
                    log.info("SERVER", f"{url} already cached")
                    return True

        log.info("SERVER", f"{url} is being cached")
        self.add_cache([url, ])

        return False

    def insert(self, urls: list[str]):
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

    def fetch(self, urls: list[str]):
        for url in urls:
            if not self.is_cached(url):
                try:
                    log.info("SERVER", f"{url} fetching...")
                    WebDriverConnection.driver.get("https://"+url)
                    content = WebDriverConnection.driver.page_source

                    with open(settings.SERVER_CACHE + util.get_hash(url.strip()), 'w+') as file:
                        file.write(content)
                        log.info("SERVER", url.strip() + ' is saved')
                except Exception as e:
                    log.error("SERVER", str(e))

    def parse(self, urls: list[str]):
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

    def refresh(self):
        try:
            DatabaseConnection.cursor.execute("""
                select url from product;
            """)
            urls = DatabaseConnection.cursor.fetchall()
            urls = [url[0] for url in urls]
            log.info("SERVER", "URLs is fetched from database")

            if urls:
                log.info("SERVER", "URLs is being refreshed")
                self.fetch(urls)
                self.parse(urls)
                self.insert(urls)
            else:
                log.info("SERVER", "Database is empty")

        except Exception as e:
            log.error("SERVER", str(e))

    def read_one(self, url: str):
        lines = self.read_cache()

        for line in lines:
            if line and line.split(',')[1] == url:
                return line

    def read_cache(self):
        with open(settings.URLS_CACHE, "r") as f:
            lines = f.read().strip().split('\n')

        return lines

    def add_cache(self, urls: list[str]):
        lines = self.read_cache()

        with open(settings.URLS_CACHE, "w") as f:
            for line in lines:
                if line:
                    url = line.split(',')[1]
                    if url not in urls:
                        f.write(line + '\n')

            for url in urls:
                f.write(f"{util.now()},{self.url_parse(url)}\n")

    def url_parse(self, url: str):
        url = urlparse(url)
        return url.netloc + url.path

    def tracking(self, params: dict):
        if "refresh" in params.keys() and params["refresh"]:
            self.refresh()
        elif "urls" in params.keys():
            urls = [self.url_parse(url) for url in params["urls"]]
            self.fetch(urls)
            self.parse(urls)
            self.insert(urls)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        params = self.body_parser(post_data)

        self.tracking(params)

        self.send_response(200)
        self.end_headers()
