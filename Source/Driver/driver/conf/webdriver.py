from abc import ABC

from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import conf.logger as log


class DriverConnection(ABC):
    service = None
    driver = None

    @staticmethod
    def init():
        if DriverConnection.driver:
            log.info("DRIVER", "already created")
            return

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("user-agent=*")
        try:
            DriverConnection.service = Service(ChromeDriverManager().install())
            DriverConnection.driver = webdriver.Chrome(
                service=DriverConnection.service, options=options)
        except Exception as e:
            log.error("Driver", str(e))

    @staticmethod
    def close():
        if DriverConnection.driver:
            DriverConnection.driver.quit()
