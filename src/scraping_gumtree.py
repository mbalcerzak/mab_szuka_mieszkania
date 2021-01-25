import requests
import json
import re
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup


def get_price(soup) -> int:
    try:
        results = soup.find('div', class_="vip-title clearfix")
        price = results.find('span', class_='amount')

        return int(re.sub("[^\d\.,]", "", price.text))
    except AttributeError:
        return 0


def get_description(soup) -> str:
    try:
        results = soup.find(id="wrapper")
        description = results.find('span', class_='pre')
        description = description.text.replace('\"', '\'').replace('\\', '')
    except AttributeError:
        description = 'NA'

    return description


def get_photos(soup):
    gallery = soup.find(id="vip-gallery-data")

    if gallery is None:
        return {"photos_links": ['No photos']}

    pattern = re.compile('\{.*\}')
    json_obj = json.loads(re.findall(pattern, str(gallery))[0])

    return json_obj['large']


def get_add_title(soup) -> str:
    results = soup.find('div', class_="vip-title clearfix")
    title = results.find('span', class_='myAdTitle').text.replace('\'', '')

    return title


def extract_num_rooms(text: str) -> int:
    if "Kawalerka" in text:
        return 1
    return int(re.sub("[^\d]", "", text))


def get_attributes(soup) -> dict:
    results = soup.find(id="wrapper")
    attributes = results.find('ul', class_='selMenu')
    attributes_all = attributes.find_all('div', class_='attribute')

    attr_dict = {}

    for elem in attributes_all:

        attr_name = (elem.find('span', class_='name')).text
        attr_val = (elem.find('span', class_='value')).text

        if attr_name not in attr_dict:
            if attr_name in ['Liczba pokoi', 'Liczba łazienek']:
                attr_val = extract_num_rooms(attr_val)
            attr_dict[attr_name] = attr_val

    return attr_dict


keys_dict = {
    'Data dodania': 'date_posted',
    'Lokalizacja': 'location',
    'Na sprzedaż przez': 'seller',
    'Rodzaj nieruchomości': 'property_type',
    'Liczba pokoi': 'num_rooms',
    'Liczba łazienek': 'num_bathrooms',
    'Wielkość (m2)': 'flat_area',
    'Parking': 'parking'}


def get_flat_info(page_address) -> dict:
    page = requests.get(page_address)
    soup = BeautifulSoup(page.content, 'html.parser')

    ad_id = page_address.split('/')[-1][3:12]
    price = get_price(soup)
    title = get_add_title(soup)
    today = datetime.today().strftime('%d/%m/%Y')
    description = get_description(soup)
    photos_links = get_photos(soup)

    flat = {'ad_id': ad_id,
            'title': title,
            'date_posted': 'NA',
            'date_scraped': today,
            'location': 'NA',
            'price': price,
            'seller': 'NA',
            'property_type': 'NA',
            'num_rooms': 0,
            'num_bathrooms': 1,
            'flat_area': 0,
            'parking': 'Brak',
            'description': description,
            'photos_links': photos_links,
            'price_history': '{}',
            'page_address': page_address
            }

    attributes = get_attributes(soup)

    for key, value in attributes.items():
        if key in keys_dict:
            key = keys_dict[key]
            flat[key] = value

    return flat


def add_flat(page_address, cursor):
    print("Adding a new flat")
    flat = get_flat_info(page_address)

    input_ = (f"INSERT INTO flats VALUES ("
              f"{flat['ad_id']}, "
              f"\'{flat['title']}\', "
              f"\'{flat['date_posted']}\', "
              f"\'{flat['date_scraped']}\', "
              f"\'{flat['location']}\', "
              f"{flat['price']}, "
              f"\'{flat['seller']}\', "
              f"\'{flat['property_type']}\', "
              f"{flat['num_rooms']}, "
              f"{flat['num_bathrooms']}, "
              f"{flat['flat_area']}, "
              f"\"{flat['parking']}\", "
              f"\"{flat['description']}\", "
              f"\"{flat['photos_links']}\", "
              f"\"{flat['price_history']}\", "
              f"\"{flat['page_address']}\""
              ")")
    cursor.execute(input_)


if __name__ == "__main__":
    # example with photos
    # ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/zoliborz/mieszkanie-warszawa-zoliborz-55m2-nr-sol+ms+137199+2/1008618526330911559470109'

    # no photos
    # ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/bielany/3-pokoje-na-zamknietym-monitorowanym-osiedlu-przy-multikinie-mlociny/1008627292720912407250109'

    # no amount
    # ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/mokotow/3-pokoje-z-balkonem/1008627031860912407250109'

    # "\" in the description
    # ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/srodmiescie/muranow-balkon-centrum-mieszkanie-z-ksiega/1008594111190911379840409'

    try:
        # conn = sqlite3.connect('../data/flats.db')
        conn = sqlite3.connect(r'C:\Users\kkql180\NonWorkProjects\mab_szuka_mieszkania\data\flats_test.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise Exception

    # no title
    # ad_link = 'https://www.gumtree.pl/a-mieszkania-i-domy-sprzedam-i-kupie/praga-polnoc/33-m2-do-wykonczenia-przedwojenna-kamienica/1008730644430912520720209'

    # "błąd w Sprzedam"
    ad_link = 'https://www.gumtree.pl/a-mieszkania-i-domy-sprzedam-i-kupie/praga-poludnie/3+pokoje-do-wejscia-super-widok-po-remoncie-kw-60m/1008747663390911379840409'
    flat_example = get_flat_info(ad_link)
    print(flat_example)

    add_flat(flat_example, cursor)
    conn.commit()
    conn.close()
