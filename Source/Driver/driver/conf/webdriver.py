from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=*")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
