# To-do
# - Scrape the entire page
# - Get the link again
# - Download the paper
# - Put the paper into a folder
# - Automatically make a spreadsheet with the paper title, the paper link, the SJR quintile, and the paper itself

import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Path to ChromeDriver installation - no relative paths
path = "/Users/Charlie/Documents/Code/webScraper/chromedriver"

# URL to be scraped
url = "https://www.scienceopen.com/search#('v'~4_'id'~''_'queryType'~1_'context'~null_'kind'~77_'order'~1_'orderLowestFirst'~false_'query'~'carbon%20capture'_'filters'~!('kind'~38_'not'~false_'offset'~2_'timeUnit'~7)*_'hideOthers'~false)"

df = pd.read_csv("scimagojr-2023.csv", sep=";", decimal=",")

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")

service = Service(path)
driver = webdriver.Chrome(service=service, options=options)

driver.get(url)
time.sleep(0.5)
pageContent = driver.page_source

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

driver = webdriver.Chrome(service=service, options=options)

for key in keys:
    driver.get(papers[key])
    # time.sleep(0.5)
    pageContent = driver.page_source
    parsedPage = soup(pageContent, "html.parser")
    issn = parsedPage.find(itemprop="issn")
    if issn != None:
        issn = issn.get_text(strip=True)
        issn = issn[0:4] + issn[5:9]
        newDf = df[df["Issn"].str.contains(issn)]
        sjr = newDf.iloc[0, 6]
        print("Link: "+ papers[key] + " with an SJR quintile of: " + str(sjr))
        if sjr != "Q1":
            del papers[key]
    else:
        del papers[key]

driver.quit()
