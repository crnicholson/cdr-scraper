# To-do
# - Scrape the entire page
# - Get the ISSN from the link
# - Input the ISSN into the SJR

import time
import csv
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
pageContent = driver.page_source
driver.quit()

parsedPage = soup(pageContent, "html.parser")
allTitles = parsedPage.find_all(class_="so-article-list-item-title")

papers = {}

for titles in allTitles:
    foundLink = titles.find("a")
    if foundLink != None:
        paperUrl = foundLink["href"]
        paperTitle = foundLink.get_text(strip=True)
        papers[paperTitle] = paperUrl

keys = list(papers)

# for key in keys:
#     driver = webdriver.Chrome(service=service, options=options)
#     driver.get(papers[key])
#     time.sleep(0.5)
#     pageContent = driver.page_source
#     driver.quit()
#     parsedPage = soup(pageContent, "html.parser")
#     issn = parsedPage.find(itemprop="issn")
#     if issn != None:
#         issn = issn.get_text(strip=True)
#         issn = issn[0:4] + issn[5:9]
#         print(issn)
#         papers[key] = issn
#     else:
#         del papers[key]

# keys = list(papers)

# print(papers)

# fields = []
# rows = []

# with open("scimagojr 2023.csv", "w") as file:
#     csvReader = csv.reader(file)

#     for row in csvReader:
#         rows.append(row)

#     print("done")

import pandas as pd

df = pd.read_csv("scimagojr-2023.csv")

print(df.head())
