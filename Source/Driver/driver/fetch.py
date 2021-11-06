import os
import hashlib

from colorama import Fore
from tqdm import tqdm
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from debug import INFO


CACHE_FOLDER = '.cache/'


def get_hash(url: str):
    hash_obj = hashlib.sha256(bytes(url, 'utf-8'))
    return hash_obj.hexdigest()


def __get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=*")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def __is_cached(fun):
    def wrapper(*args, **kwargs):
        url = args[0]
        content_file = get_hash(url)

        if not os.path.exists(CACHE_FOLDER + content_file):
            INFO(content_file, "not found in cache", tc=Fore.RED)
            return fun(url=args[0])

        INFO(content_file, "found in cache")

        cached_content = ""
        with open(CACHE_FOLDER + content_file, "r") as content:
            cached_content = content.read()

        return fun(url, cached_content)

    return wrapper


def __save_content(url: str, content: str) -> bool:
    content_file = get_hash(url)

    try:
        with open(CACHE_FOLDER + content_file, "w+") as file:
            file.write(content)
    except:
        return False

    return True


@__is_cached
def get_content(url: str, cached_content: str = None) -> str:
    global driver

    if not cached_content:
        driver.get(url)

        content = driver.page_source
        if not __save_content(url, content):
            print("Content doesn't saved")
        else:
            return content
    else:
        return cached_content


driver = __get_driver()
