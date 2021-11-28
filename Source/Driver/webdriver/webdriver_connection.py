import os

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager

import log


class WebDriverConnection:
    _instance = None
    _service = None
    _driver = None

    capabilities = DesiredCapabilities.CHROME.copy()
    capabilities["acceptInsecureCerts"] = True

    chrome_options = Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("user-agent=*")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebDriverConnection, cls).__new__(cls)

        if not cls._service:
            try:
                cls._service = Service(ChromeDriverManager().install())

                if not cls._driver:
                    cls._driver = webdriver.Chrome(
                        service=cls._service, options=cls.chrome_options, desired_capabilities=cls.capabilities)
                    log.info("WEBDRIVER", "Service & Driver is created",
                             fore=log.Fore.LIGHTGREEN_EX)
                else:
                    log.info("WEBDRIVER", "Service & Driver is already created",
                             fore=log.Fore.LIGHTGREEN_EX)
            except Exception as e:
                log.error(
                    "WEBDRIVER", "Service & Driver is not created __> " + str(e))

        return cls._instance

    @classmethod
    @property
    def status(cls):
        return (cls._driver and cls._service) is not None

    @classmethod
    @property
    def driver(cls):
        return cls._driver

    @classmethod
    def close(cls):
        if cls._driver:
            cls._driver.quit()
