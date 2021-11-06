import os
import pprint
import hashlib

from colorama import Fore, Back, Style
from tqdm import tqdm
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


CACHE_FOLDER = '.cache/'

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("user-agent=*")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver

def get_hash(url: str):
    hash_obj = hashlib.sha256(bytes(url, 'utf-8'))
    return hash_obj.hexdigest()

def is_cached(fun):
    def wrapper(*args, **kwargs):
        url = args[0]
        content_file = get_hash(url)

        if not os.path.exists(CACHE_FOLDER + content_file):
            print(Fore.YELLOW + "[INFO] " + Style.RESET_ALL + Fore.RED + content_file + Style.RESET_ALL + " not found in cache")
            return fun(url=args[0])

        print(Fore.YELLOW + "[INFO] " + Style.RESET_ALL + Fore.GREEN + content_file + Style.RESET_ALL + " found in cache")

        cached_content = ""
        with open(CACHE_FOLDER + content_file, "r") as content:
            cached_content = content.read()

        return fun(url, cached_content)

    return wrapper

def save_content(url: str, content: str) -> bool:
    content_file = get_hash(url)

    with open(CACHE_FOLDER + content_file, "w+") as file:
        file.write(content)

    return True

@is_cached
def get_content(url: str, cached_content: str = None) -> str:
    global driver

    if not cached_content:
        driver.get(url)

        content = driver.page_source
        if not save_content(url, content):
            print("Content doesn't saved")
        else:
            return content
    else:
        return cached_content


driver = get_driver()
