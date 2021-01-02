from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json
import re
import sqlite3

#TODO at some point make it run faster

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
    def __init__(self, ad_id, price, title, **kwargs):
        self.ad_id = ad_id
        self.price = price
        self.title = title

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

        price_history = {today: price}
        self.price_history = str(price_history)

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
    print(title)

    description = get_description(soup)
    photos_links = get_photos(soup)
    attributes = get_attributes(soup)

    ad_attributes = attributes | description | photos_links

    return Flat(ad_id, price, title, **ad_attributes)


def check_if_id_exists(cursor, flat):
    cursor.execute(f'SELECT * FROM flats WHERE ad_id = {flat.ad_id}')
    return True if len(cursor.fetchall()) != 0 else False


def check_if_price_changed(cursor, flat):
    new_price = int(flat.price)
    cursor.execute(f'SELECT price FROM flats WHERE ad_id = {flat.ad_id}')
    old_price = cursor.fetchone()[0]

    today = datetime.today().strftime('%d/%m/%Y')

    if old_price != new_price:
        print(f"{old_price=} is different than the {new_price=}")

        cursor.execute(f'SELECT price_history FROM flats WHERE ad_id = {flat.ad_id}')
        price_history = cursor.fetchone()[0]
        price_history = eval(price_history)

        if str(today) not in price_history:
            price_history[today] = new_price

            cursor.execute(f"UPDATE flats SET price_history = \"{price_history}\""
                           f" WHERE ad_id = {flat.ad_id}")

        cursor.execute(f'UPDATE flats SET price = {flat.price} ' 
                       f'WHERE ad_id = {flat.ad_id}')
    else:
        print("This flat still has the same price, all good")

    cursor.execute(f'UPDATE flats SET date_scraped = \'{today}\' ' 
                   f'WHERE ad_id = {flat.ad_id}')


def add_flat(flat):
    if flat.price is None:
        return None
    try:
        conn = sqlite3.connect('../data/flats.db')
        cursor = conn.cursor()
        print("Connected to SQLite")
    except sqlite3.Error as e:
        raise Exception

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
                   f"\"{flat.price_history}\""
                   ")")

    if check_if_id_exists(cursor, flat):
        print(f"Row with that ID ({flat.ad_id}) already is in the database, "
              f"checking if the price changed")
        check_if_price_changed(cursor, flat)
        try:
            conn.commit()
        except sqlite3.Error as e:
            print(e)
    else:
        try:
            cursor.execute(input_)
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        print("New input added successfully")

    conn.close()


if __name__ == "__main__":
    # example with photos
    # ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/zoliborz/mieszkanie-warszawa-zoliborz-55m2-nr-sol+ms+137199+2/1008618526330911559470109'

    # no photos
    # ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/bielany/3-pokoje-na-zamknietym-monitorowanym-osiedlu-przy-multikinie-mlociny/1008627292720912407250109'

    # no amount
    ad_link = '/a-mieszkania-i-domy-sprzedam-i-kupie/mokotow/3-pokoje-z-balkonem/1008627031860912407250109'

    flat1 = get_flat_info(ad_link)
    flat1.show_attr()

    add_flat(flat1)
