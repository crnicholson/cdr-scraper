# import requests 
# from bs4 import BeautifulSoup 

# page = requests.get("https://www.scienceopen.com/search#('v'~4_'id'~''_'queryType'~1_'context'~null_'kind'~77_'order'~0_'orderLowestFirst'~false_'query'~'carbon%20removal'_'filters'~!('kind'~37_'not'~false_'dateFrom'~1641013200000_'dateTo'~1717300799999)*_'hideOthers'~false)") 

# soup = BeautifulSoup(page.content, 'html.parser') 

# results = soup.find(id="d4777409e111")

# print(results)

import requests
from bs4 import BeautifulSoup

page = requests.get("https://webscraper.io/test-sites/e-commerce/allinone")

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find_all(class_="nav-link")

for results in results:
    found = results.find("p")
    string = str(found)
    if found != None:
        length = len(string)
        string = string[3:length-4]
        print(string)
