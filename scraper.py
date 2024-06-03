import time
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

path = "/Users/Charlie/Documents/Code/webScraper/chromedriver"

# URL to be scraped
url = "https://www.scienceopen.com/search"

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

service = Service(path)
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)

time.sleep(0.5)

content = driver.page_source

driver.quit()

page = soup(content, "html.parser")

page = page.prettify()

f  = open("page.txt", "w")
f.write(page)
f.close()
