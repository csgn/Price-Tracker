from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import log


class WebDriverConnection:
    _instance = None
    _service = None
    _driver = None

    __options = Options()
    __options.add_argument("--headless")
    __options.add_argument("--no-sandbox")
    __options.add_argument("user-agent=*")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebDriverConnection, cls).__new__(cls)

        if not cls._service:
            try:
                cls._service = Service(ChromeDriverManager().install())

                if not cls._driver:
                    cls._driver = webdriver.Chrome(
                        service=cls._service, options=cls.__options)

                log.info("WEBDRIVER", "Service & Driver is created",
                         fore=log.Fore.LIGHTGREEN_EX)
            except Exception as e:
                log.error(
                    "WEBDRIVER", "Service & Driver is not created __> " + str(e))

        return cls._instance

    @classmethod
    @property
    def status(cls):
        return cls._driver is not None

    @classmethod
    @property
    def driver(cls):
        return cls._driver

    @classmethod
    def close(cls):
        if cls._driver:
            cls._driver.quit()
