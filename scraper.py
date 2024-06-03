import time
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.chrome.options import Options

path = "chromedriver"
url = "https://www.scienceopen.com/search"

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(path, options=options)

time.sleep(5)

driver.get(url)

content = driver.page_source

driver.quit()

page = soup(content, 'html.parser')

print(page.prettify())
