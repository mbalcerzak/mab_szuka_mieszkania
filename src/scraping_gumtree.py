import requests
from bs4 import BeautifulSoup
import json
import re


def get_description(soup):
    results = soup.find(id="wrapper")
    description = results.find('div', class_='description')

    return description.text


def get_photos(soup):
    gallery = soup.find(id="vip-gallery-data")
    pattern = re.compile('\{.*\}')
    json_obj = json.loads(re.findall(pattern, str(gallery))[0])

    return dict(zip(json_obj['alt-tags'], json_obj['large']))


def get_attributes(soup):
    results = soup.find(id="wrapper")
    attributes = results.find('ul', class_='selMenu')
    attributes2 = attributes.find_all('div', class_='attribute')

    attr_dict = {}

    for elem in attributes2:

        attr_name = (elem.find('span', class_='name')).text
        attr_val = (elem.find('span', class_='value')).text

        if attr_name not in attr_dict:
            attr_dict[attr_name] = attr_val

    return attr_dict


def get_flat_info(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    description = get_description(soup)
    photos_links = get_photos(soup)
    attributes = get_attributes(soup)
    id = link.split('/')[-1]

    return [id, attributes, description, photos_links]


ad_link = 'https://www.gumtree.pl/a-mieszkania-i-domy-sprzedam-i-kupie/srodmiescie/mieszkanie-2-pokojowe-piekna-okolica/1006938050400911260981009'
print(get_flat_info(ad_link))