import os

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import conf.global_settings as settings
import conf.webdriver as driver
import conf.scripts.util as util
import conf.logger as log


def __is_cached(fun):
    def wrapper(*args, **kwargs):
        url = args[0]
        content_file = util.get_hash(url)

        if not os.path.exists(settings.CACHE_FOLDER + content_file):
            log.warning(content_file, "not found in cache", fore=log.Fore.RED)
            return fun(url=args[0])

        log.info(content_file, "found in cache", fore=log.Fore.LIGHTGREEN_EX)

        cached_content = ""
        with open(settings.CACHE_FOLDER + content_file, "r") as content:
            cached_content = content.read()

        return fun(url, cached_content)

    return wrapper


def __save_content(url: str, content: str) -> bool:
    content_file = util.get_hash(url)

    try:
        with open(settings.CACHE_FOLDER + content_file, "w+") as file:
            file.write(content)
    except:
        return False

    return True


@__is_cached
def get(url: str, cached_content: str = None) -> str:
    content_file = util.get_hash(url)

    if not cached_content:
        log.info(content_file, "fetching...", fore=log.Fore.LIGHTMAGENTA_EX)
        driver.driver.get(url)

        content = driver.driver.page_source

        if not __save_content(url, content):
            log.warning(content_file, "is not saved")
            pass
        else:
            log.info(content_file, "was fetched", fore=log.Fore.LIGHTGREEN_EX)
            return content
    else:
        return cached_content
