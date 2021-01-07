import requests
import json
import re
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup


def get_price(soup) -> str:
    results = soup.find('div', class_="vip-title clearfix")
    price = results.find('span', class_='amount')

    return re.sub("[^\d\.,]", "", price.text)


def get_description(soup) -> dict:
    results = soup.find(id="wrapper")
    description = results.find('span', class_='pre')

    return {"description": description.text.replace('\"', '\'')}


def get_photos(soup) -> dict:
    gallery = soup.find(id="vip-gallery-data")

    if gallery is None:
        return {"photos_links": ['No photos']}

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
    'Data dodania': 'date_posted',
    'Lokalizacja': 'location',
    'Na sprzedaż przez': 'seller',
    'Rodzaj nieruchomości': 'property_type',
    'Liczba pokoi': 'num_rooms',
    'Liczba łazienek': 'num_bathrooms',
    'Wielkość (m2)': 'flat_area',
    'Parking': 'parking'}


class Flat:
    def __init__(self, ad_id, price, title, link, **kwargs):
        self.ad_id = ad_id
        self.price = price
        self.title = title
        self.page_address = link

        self.description = 'NA'
        self.date_posted = 'NA'
        self.seller = 'NA'
        self.property_type = 'NA'
        self.num_rooms = 0
        self.num_bathrooms = 1
        self.flat_area = 0
        self.parking = 'Brak'

        today = datetime.today().strftime('%d/%m/%Y')
        self.date_scraped = today
        self.price_history = '{}'

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
    try:
        price = get_price(soup)
    except AttributeError:
        return None

    title = get_add_title(soup)

    description = get_description(soup)
    photos_links = get_photos(soup)
    attributes = get_attributes(soup)

    ad_attributes = attributes | description | photos_links

    return Flat(ad_id, price, title, link, **ad_attributes)


def check_if_id_exists(cursor, flat):
    cursor.execute(f'SELECT * FROM flats WHERE ad_id = {flat.ad_id}')
    return True if len(cursor.fetchall()) != 0 else False


def check_if_price_changed(cursor, flat):
    new_price = int(flat.price)
    cursor.execute(f'SELECT price FROM flats WHERE ad_id = {flat.ad_id}')
    old_price = int(cursor.fetchone()[0])

    if old_price != new_price:
        print(f"{old_price=} and {new_price=} are different")
        update_price(cursor, flat, old_price, new_price)


def update_price(cursor, flat, old_price, new_price):
    today = datetime.today().strftime('%d/%m/%Y')
    cursor.execute(f'SELECT price_history FROM flats '
                   f'WHERE ad_id = {flat.ad_id}')
    price_history = eval(cursor.fetchone()[0])

    cursor.execute(f'SELECT date_scraped FROM flats '
                   f'WHERE ad_id = {flat.ad_id}')
    previous_date = cursor.fetchone()[0]

    if str(previous_date) not in price_history:
        price_history[previous_date] = old_price

    if str(today) not in price_history:
        price_history[today] = new_price

    cursor.execute(f"UPDATE flats "
                   f"SET price_history = \"{price_history}\", "
                   f"    price = {new_price}, "
                   f"    date_scraped = \'{today}\'"
                   f"WHERE ad_id = {flat.ad_id}")


# TODO remove one day - temporary solution
def check_if_page_address_exists(cursor, flat):
    cursor.execute(f'SELECT page_address FROM flats WHERE ad_id = {flat.ad_id}')
    return False if len(cursor.fetchone()[0]) == 0 else True


def update_page_address_empty(cursor, flat):
    cursor.execute(f'UPDATE flats SET page_address = \"{flat.page_address}\" ' 
                   f'WHERE ad_id = {flat.ad_id}')
    print("Page address was missing - added")


def add_flat(flat):
    try:
        x = flat.price
        # TODO poprawić tę paskudę
    except AttributeError:
        print("Invalid price, skipping the ad")
        return None
    try:
        conn = sqlite3.connect('../data/flats.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise Exception

    if check_if_id_exists(cursor, flat):
        print(f"Row with that ID ({flat.ad_id}) already is in the database")

        if not check_if_page_address_exists(cursor, flat):
            update_page_address_empty(cursor, flat)
            conn.commit()

        check_if_price_changed(cursor, flat)

    else:
        input_ = (f"INSERT INTO flats VALUES ("
                  f"{flat.ad_id}, "
                  f"'{flat.title}', "
                  f"'{flat.date_posted}', "
                  f"'{flat.date_scraped}', "
                  f"'{flat.location}', "
                  f"{flat.price}, "
                  f"'{flat.seller}', "
                  f"'{flat.property_type}', "
                  f"{flat.num_rooms}, "
                  f"{flat.num_bathrooms}, "
                  f"{flat.flat_area}, "
                  f"'{flat.parking}', "
                  f"\"{flat.description}\", "
                  f"\"{flat.photos_links}\", "
                  f"\"{flat.price_history}\", "
                  f"\"{flat.page_address}\""
                  ")")
        cursor.execute(input_)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # example with photos
    # ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/zoliborz/mieszkanie-warszawa-zoliborz-55m2-nr-sol+ms+137199+2/1008618526330911559470109'

    # no photos
    # ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/bielany/3-pokoje-na-zamknietym-monitorowanym-osiedlu-przy-multikinie-mlociny/1008627292720912407250109'

    # no amount
    # ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/mokotow/3-pokoje-z-balkonem/1008627031860912407250109'

    # "\" in the description
    ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/srodmiescie/muranow-balkon-centrum-mieszkanie-z-ksiega/1008594111190911379840409'

    flat_example = get_flat_info(ad_link)
    flat_example.show_attr()

    add_flat(flat_example)
