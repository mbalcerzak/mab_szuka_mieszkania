import requests
from bs4 import BeautifulSoup
import json
import re
import sqlite3


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

    return {"photos_links": json_obj['large']}


def get_add_title(soup) -> str:
    results = soup.find('div', class_="vip-title clearfix")
    title = results.find('span', class_='myAdTitle')

    return title.text


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
    def __init__(self, ad_id, price, title, **kwargs):
        self.ad_id = ad_id
        self.price = price
        self.title = title

        self.description = 'NA'
        self.date_added = 'NA'
        self.seller = 'NA'
        self.property_type = 'NA'
        self.num_rooms = 0
        self.num_bathrooms = 1
        self.flat_area = 0
        self.parking = 'Brak'

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
    title = get_add_title(soup)

    description = get_description(soup)
    photos_links = get_photos(soup)
    attributes = get_attributes(soup)

    ad_attributes = attributes | description | photos_links

    return Flat(ad_id, price, title, **ad_attributes)


def add_flat(flat):
    try:
        conn = sqlite3.connect('../data/flats.db')
        cursor = conn.cursor()
        print("Connected to SQLite")
    except sqlite3.Error as e:
        raise Exception

    input_ = (f"INSERT INTO flats VALUES ("
                   f"{flat.ad_id}, "
                   f"'{flat.title}', "
                   f"'{flat.date_added}', "
                   f"'{flat.location}', "
                   f"{flat.price}, "
                   f"'{flat.seller}', "
                   f"'{flat.property_type}', "
                   f"{flat.num_rooms}, "
                   f"{flat.num_bathrooms}, "
                   f"{flat.flat_area}, "
                   f"'{flat.parking}', "
                   f"\"{flat.description}\", "
                   f"\"{flat.photos_links}\""
                   ")")

    try:
        cursor.execute(input_)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

    # cursor.execute('SELECT * FROM flats')
    # print(cursor.fetchone())

    conn.close()


if __name__ == "__main__":
    ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/zoliborz/mieszkanie-warszawa-zoliborz-55m2-nr-sol+ms+137199+2/1008618526330911559470109'
    flat1 = get_flat_info(ad_link)
    flat1.show_attr()
