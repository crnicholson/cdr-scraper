from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup

url = "https://doaj.org/search/articles?ref=homepage-box&source=%7B%22query%22%3A%7B%22bool%22%3A%7B%22must%22%3A%5B%7B%22range%22%3A%7B%22index.date%22%3A%7B%22lt%22%3A%221704067200000%22%2C%22gte%22%3A%221672531200000%22%2C%22format%22%3A%22epoch_millis%22%7D%7D%7D%2C%7B%22query_string%22%3A%7B%22query%22%3A%22carbon%20removal%22%2C%22default_operator%22%3A%22AND%22%7D%7D%5D%7D%7D%2C%22track_total_hits%22%3Atrue%7D"

req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
webpage = urlopen(req).read()

page = soup(webpage, 'html.parser')

print(page.prettify())