import time
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to ChromeDriver installation - no relative paths
path = "/Users/Charlie/Documents/Code/webScraper/chromedriver"

# URL to be scraped
url = "https://www.scienceopen.com/search#('v'~4_'id'~''_'queryType'~1_'context'~null_'kind'~77_'order'~1_'orderLowestFirst'~false_'query'~'carbon%20capture'_'filters'~!('kind'~38_'not'~false_'offset'~2_'timeUnit'~7)*_'hideOthers'~false)"

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

results = page.find_all(class_="so-article-list-item-title")

for result in results:
    print(result.prettify())
    found = result.find("p")
    if found is not None:
        string = found.get_text(strip=True)
        print(string)

with open("page.txt", "w") as f:
    f.write(page.prettify())
