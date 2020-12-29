import requests
from bs4 import BeautifulSoup
import json
import re




# przykładowy adres ogłoszenia:
# ad_link = "https://www.gumtree.pl/a-mieszkania-i-domy-sprzedam-i-kupie/bielany/4-pokojowe-mieszkanie-bielany-ul-kochanowskiego/1008615130830911378860309"

ad_link = 'https://www.gumtree.pl/a-mieszkania-i-domy-sprzedam-i-kupie/srodmiescie/mieszkanie-2-pokojowe-piekna-okolica/1006938050400911260981009'

# ad_link = 'https://www.gumtree.pl/a-mieszkania-i-domy-sprzedam-i-kupie/rembertow/135m-%252Bogrodek-oddzielne-wejscie-5min-do-pkp-200m-do-autobusu-roi-10/1008614496810910556456609'

page = requests.get(ad_link)
soup = BeautifulSoup(page.content, 'html.parser')

### description ##########################
results = soup.find(id="wrapper")
description = results.find('div', class_='description')
print(description.text)


#### photos ######################
gallery = soup.find(id="vip-gallery-data")
pattern = re.compile('\{.*\}')
json_obj = json.loads(re.findall(pattern, str(gallery))[0])

print(json_obj['large'])


# #### - cenę mieszkania #############
# - lokalizację
# - wielkość mieszkania
# - które piętro

attributes = results.find('ul', class_='selMenu')
attributes2 = attributes.find_all('div', class_='attribute')

for elem in attributes2:

    klucz = (elem.find('span', class_='name')).text
    wartosc = (elem.find('span', class_='value')).text
    print(klucz, wartosc)


#### ID ogłoszenia
print(ad_link.split('/')[-1])

# class Mieszkanie:
