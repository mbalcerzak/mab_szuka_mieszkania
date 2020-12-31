import requests
from bs4 import BeautifulSoup
import json
import re


def get_price(soup) -> str:
    results = soup.find('div', class_="vip-title clearfix")
    price = results.find('span', class_='amount')

    return re.sub("[^\d\.,]", "", price.text)


def get_description(soup) -> dict:
    results = soup.find(id="wrapper")
    description = results.find('span', class_='pre')

    return {"description": description.text}


def get_photos(soup) -> dict:
    gallery = soup.find(id="vip-gallery-data")
    pattern = re.compile('\{.*\}')
    json_obj = json.loads(re.findall(pattern, str(gallery))[0])

    return {"photos_links": dict(zip(json_obj['alt-tags'], json_obj['large']))}


def extract_num(text: str) -> int:
    if "Kawalerka" in text:
        return 1
    return re.sub("[^\d]", "", text)


def get_attributes(soup) -> dict:
    results = soup.find(id="wrapper")
    attributes = results.find('ul', class_='selMenu')
    attributes2 = attributes.find_all('div', class_='attribute')

    attr_dict = {}

    for elem in attributes2:

        attr_name = (elem.find('span', class_='name')).text
        attr_val = (elem.find('span', class_='value')).text

        if attr_name not in attr_dict:
            if attr_name in ['Liczba pokoi', 'Liczba łazienek']:
                attr_val = extract_num(attr_val)
            attr_dict[attr_name] = attr_val

    return attr_dict


keys_dict = {
    'Data dodania': 'date_added',
    'Lokalizacja': 'location',
    'Na sprzedaż przez': 'seller',
    'Rodzaj nieruchomości': 'property_type',
    'Liczba pokoi': 'num_rooms',
    'Liczba łazienek': 'num_bathrooms',
    'Wielkość (m2)': 'flat_area',
    'Parking': 'parking'}


class Flat:
    def __init__(self, ad_id, price, **kwargs):
        self.ad_id = ad_id
        self.price = price

        self.description = 'NA'
        self.date_added = 'NA'
        self.seller = 'NA'
        self.property_type = 'NA'
        self.num_rooms = 0
        self.num_bathrooms = 1
        self.flat_area = 0
        self.parking = 'NA'

        for key, value in kwargs.items():
            if key in keys_dict:
                key = keys_dict[key]
            setattr(self, key, value)

    def show_attr(self):
        print(vars(self))


def get_flat_info(link) -> list:
    link = f'https://www.gumtree.pl{link}'

    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    ad_id = link.split('/')[-1][3:12]
    price = get_price(soup)

    description = get_description(soup)
    photos_links = get_photos(soup)
    attributes = get_attributes(soup)

    ad_attributes = attributes | description | photos_links

    return Flat(ad_id, price, **ad_attributes)


if __name__ == "__main__":
    ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/zoliborz/mieszkanie-warszawa-zoliborz-55m2-nr-sol+ms+137199+2/1008618526330911559470109'
    flat = get_flat_info(ad_link)
    flat.show_attr()
