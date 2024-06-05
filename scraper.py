# To-do
# - Scrape the entire page
# - Get the link again
# - Download the paper
# - Put the paper into a folder
# - Automatically make a spreadsheet with the paper title, the paper link, the SJR quintile, and the paper itself

import time
import os
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path

cwd = str(Path.cwd())

def wait_for_downloads():
    print("Waiting for downloads", end="")
    while any(
        [
            filename.endswith(".crdownload")
            for filename in os.listdir(
                "/Users/Charlie/Documents/Code/webScraper/papers"
            )
        ]
    ):
        time.sleep(.5)
        print(".", end="")
    print(" Done!")

# URL to be scraped
url = "https://www.scienceopen.com/search#('v'~4_'id'~''_'queryType'~1_'context'~null_'kind'~77_'order'~1_'orderLowestFirst'~false_'query'~'carbon%20capture'_'filters'~!('kind'~38_'not'~false_'offset'~2_'timeUnit'~7)*_'hideOthers'~false)"

df = pd.read_csv("scimagojr-2023.csv", sep=";", decimal=",")

options = Options()
options.add_argument("--headless")
# options.add_argument("--disable-gpu")
options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": cwd + "/papers", 
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    },
)

service = Service(ChromeDriverManager().install())
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

print("Done finding papers.")

url = "https://www.scienceopen.com/document?vid=af69a724-0f56-4e4a-aaa9-7bde2f866333"

vid = url[41:]

downloadUrl = (
    "https://www.scienceopen.com/document?-1.ILinkListener-header-action~bar-download~dropdown-pdf~link-link&vid="
    + vid
)

driver.get(downloadUrl)
wait_for_downloads()

driver.quit()
