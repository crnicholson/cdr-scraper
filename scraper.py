# To-do
# - Scrape the entire page

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as soup
import concurrent.futures
import os

# URL to be scraped
url = "https://www.scienceopen.com/search#('v'~4_'id'~''_'queryType'~1_'context'~null_'kind'~77_'order'~1_'orderLowestFirst'~false_'query'~'carbon%20capture'_'filters'~!('kind'~38_'not'~false_'offset'~2_'timeUnit'~7)*_'hideOthers'~false)"

# Load SJR data
df = pd.read_csv("scimagojr-2023.csv", sep=";", decimal=",")

options = Options()
options.add_argument("--headless")
options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": "/Users/Charlie/Documents/Code/webScraper/papers",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
    },
)

chrome_driver_path = ChromeDriverManager().install()

def setup_driver():
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

main_driver, main_wait = setup_driver()

main_driver.get(url)
main_wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "so-article-list-item-title"))
)
pageContent = main_driver.page_source
parsedPage = soup(pageContent, "html.parser")
allTitles = parsedPage.find_all(class_="so-article-list-item-title")

papers = {}

for titles in allTitles:
    foundLink = titles.find("a")
    if foundLink:
        paperUrl = foundLink["href"]
        paperTitle = foundLink.get_text(strip=True)
        papers[paperTitle] = paperUrl

keys = list(papers)

def process_paper(key):
    driver, wait = setup_driver()
    driver.get(papers[key])
    pageContent = driver.page_source
    parsedPage = soup(pageContent, "html.parser")
    issn = parsedPage.find(itemprop="issn")
    sjr_quintile = None

    if issn:
        issn = issn.get_text(strip=True).replace("-", "")
        newDf = df[df["Issn"].str.contains(issn)]
        if not newDf.empty:
            sjr_quintile = newDf.iloc[0, 6]
            if sjr_quintile != "Q1":
                driver.quit()
                return None

    vid = papers[key][41:]
    downloadUrl = f"https://www.scienceopen.com/document?-1.ILinkListener-header-action~bar-download~dropdown-pdf~link-link&vid={vid}"
    driver.get(downloadUrl)
    # wait_for_downloads()
    time.sleep(15)
    driver.quit()
    return key, papers[key], sjr_quintile

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
    print("done!")

results = []

with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_paper = {executor.submit(process_paper, key): key for key in keys}
    for future in concurrent.futures.as_completed(future_to_paper):
        result = future.result()
        if result:
            results.append(result)

result_df = pd.DataFrame(results, columns=["Title", "Link", "SJR Quintile"])

result_df.to_csv("papers_info.csv", index=False)

main_driver.quit()
