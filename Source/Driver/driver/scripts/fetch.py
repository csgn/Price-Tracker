import os

import settings
import log

from scripts import util

from webdriver.webdriver_connection import WebDriverConnection


def __is_cached(fun):
    def wrapper(*args, **kwargs):
        url = args[0]
        content_file = util.get_hash(url)

        if not os.path.exists(settings.WEBDRIVER_CACHE + content_file):
            log.warning(content_file, "not found in cache")
            return fun(url=args[0])

        log.info(content_file, "found in cache", fore=log.Fore.LIGHTGREEN_EX)

        cached_content = ""
        with open(settings.WEBDRIVER_CACHE + content_file, "r") as content:
            cached_content = content.read()

        return fun(url, cached_content)

    return wrapper


def __save_content(url: str, content: str) -> bool:
    content_file = util.get_hash(url)

    try:
        with open(settings.WEBDRIVER_CACHE + content_file, "w+") as file:
            file.write(content)
    except Exception as e:
        log.error("FETCH", str(e))
        return False

    return True


@__is_cached
def run(url: str, cached_content: str = None) -> str:
    content_file = util.get_hash(url)

    if not cached_content:
        log.info(content_file, "fetching...", fore=log.Fore.LIGHTMAGENTA_EX)
        WebDriverConnection.driver.get(url)

        content = WebDriverConnection.driver.page_source

        if not __save_content(url, content):
            log.warning(content_file, "is not saved")
        else:
            log.info(content_file, "was fetched", fore=log.Fore.LIGHTGREEN_EX)
            return content
    else:
        return cached_content
