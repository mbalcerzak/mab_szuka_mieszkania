import requests
from bs4 import BeautifulSoup
import json
import re

ad_link = 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/warszawa/mieszkanie/v1c9073l3200008a1dwp1'


page = requests.get(ad_link)
soup = BeautifulSoup(page.content, 'html.parser')

### description ##########################
results = soup.find(id="wrapper")
description = results.find_all('a', class_="arrows icon-right-arrow icon-angle-right-gray")

# next_page = response.css('span.pag-box a::attr("href")').get()
print(description)