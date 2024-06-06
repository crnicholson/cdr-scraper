# To-do:
# - Rename the file of the paper to the title of the paper
# - Input data into ChatGPT

import time
import math
import os
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as soup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException,
)

cwd = str(Path.cwd())

##### Settings #####

maximumPageLoads = 10

# URL to be scraped
url = "https://www.scienceopen.com/search#('v'~4_'id'~''_'queryType'~1_'context'~null_'kind'~77_'order'~1_'orderLowestFirst'~false_'query'~'carbon%20capture'_'filters'~!('kind'~38_'not'~false_'offset'~2_'timeUnit'~7)*_'hideOthers'~false)"

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": cwd + "/papers",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    },
)

##### End settings #####

##### Functions #####


def waitForDownloads():
    print("Waiting for downloads", end="")
    while any(
        [
            filename.endswith(".crdownload")
            for filename in os.listdir(
                "/Users/Charlie/Documents/Code/webScraper/papers"
            )
        ]
    ):
        time.sleep(0.5)
        print(".", end="")
    print(" done!")


def getTotalSearchResults():
    WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located(
            (
                By.XPATH,
                '/html/body/div[3]/div/div/div/div/div/div[2]/div/div[5]/div[1]/div/div[@class="so-b3-label so--borderless so--gray-5 so--secondary"]',
            )
        )
    )

    searchResults = driver.find_element(
        By.XPATH,
        '/html/body/div[3]/div/div/div/div/div/div[2]/div/div[5]/div[1]/div/div[@class="so-b3-label so--borderless so--gray-5 so--secondary"]',
    )
    searchResults = str(searchResults.text)
    searchResults = int(searchResults.replace(" results", ""))

    return searchResults


def loadAllResults():
    searchResults = getTotalSearchResults()
    searchResults = math.ceil(searchResults / 10)

    if searchResults > maximumPageLoads:
        searchResults = maximumPageLoads

    print("\nLoading " + str(searchResults) + " pages of results. This may take a while.\n")

    xpath = '//*[@id="id1"]/div/div/div/div[2]/div/div[6]/div[2]/div/button[1]'
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    print("Button is visible.\n")

    i = 0
    while i < searchResults:
        i += 1
        try:
            more = driver.find_element(By.XPATH, xpath)
            more.click()
            print("Clicked the button.")
            time.sleep(5)
        except ElementClickInterceptedException:
            print("Failed to click the button.")

    return 0


##### End functions #####

df = pd.read_csv("scimagojr-2023.csv", sep=";", decimal=",")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
time.sleep(1)

driver.get(url)

# Accept cookies
driver.find_element(
    By.XPATH, "/html/body/aside/div/div/div[2]/div[2]/div/div[2]/div[1]/button[1]"
).click()

loadAllResults()

pageContent = driver.page_source
parsedPage = soup(pageContent, "html.parser")
allTitles = parsedPage.find_all(class_="so-article-list-item-title")

papers = {}
totalPapers = 0

for titles in allTitles:
    foundLink = titles.find("a")
    if foundLink != None:
        totalPapers += 1
        paperUrl = foundLink["href"]
        paperTitle = foundLink.get_text(strip=True)
        paperTitle = paperTitle.replace("\n", " ")
        # print("Found: " + paperTitle + " with URL: " + paperUrl)
        papers[paperTitle] = paperUrl

print("\nTotal papers found: " + str(totalPapers) + "\n")

titles = list(papers)

for title in titles:
    driver.get(papers[title])
    pageContent = driver.page_source
    parsedPage = soup(pageContent, "html.parser")
    issn = parsedPage.find(itemprop="issn")
    if issn != None:
        issn = issn.get_text(strip=True)
        issn = issn[0:4] + issn[5:9]
        newDf = df[df["Issn"].str.contains(issn)]
        try:
            sjr = newDf.iloc[0, 6]
            print("Paper: " + title + " with an SJR quintile of: " + str(sjr))
            if sjr != "Q1":
                del papers[title]
        except IndexError:
            del papers[title]
    else:
        del papers[title]

print("\nDone finding SJR quintile of papers.")

print(
    "\nDownloading",
    len(papers),
    "papers. " + str(totalPapers - len(papers)) + " papers were purged.",
)

print(
    "Downloading papers will take some time. It is recommended to move to a place with better WiFi.\n"
)

titles = list(papers)

for title in titles:
    url = papers[title]
    print("Downloading: " + title)
    vid = url[41:]
    downloadUrl = (
        "https://www.scienceopen.com/document?-1.ILinkListener-header-action~bar-download~dropdown-pdf~link-link&vid="
        + vid
    )
    driver.get(downloadUrl)
    waitForDownloads()

print("\nDone downloading papers.")

driver.quit()
