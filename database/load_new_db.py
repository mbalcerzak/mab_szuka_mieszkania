from os import linesep
import sqlite3
import json
from collections import defaultdict
import pandas as pd


def change_date_str(text: str) -> str:
    if "/" in text:
        dd,mm,yyyy = text.split('/')
        return f"{yyyy}-{mm}-{dd}"
    else:
        return text


def write_dict_ids():
    try:
        conn = sqlite3.connect('../data/flats1.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise Exception

    cursor.execute("SELECT ad_id, page_address FROM flats")
    list_flats = cursor.fetchall()

    dict_id = {}

    for elem in list_flats:
        ad_id = elem[0]
        page_id = elem[1].split('/')[-1]
        dict_id[ad_id] = page_id

    with open('../data/id_dict.json', 'w') as f:
        json.dump(dict_id, f)


def change_id_longer():
    try:
        conn = sqlite3.connect('../data/flats1.db')
        c = conn.cursor()
    except sqlite3.Error as e:
        raise Exception

    pd_flats = pd.read_sql("SELECT * FROM flats", conn)
    pd_prices = pd.read_sql("SELECT * FROM prices", conn)

    with open('../data/id_dict.json', 'r') as f:
        ids_json = json.load(f)

    print(pd_flats.head())
    print(pd_prices.head())

    foreign_ids = dict(zip(pd_flats["ad_id"], pd_flats.index))
    # print(foreign_ids)

    pd_flats["ad_id"] = pd_flats["ad_id"].apply(lambda x: ids_json[str(x)])
    pd_flats['flat_id'] = pd_flats.index

    pd_prices["flat_id"] = pd_prices["flat_id"].apply(lambda x: foreign_ids[x])
    # pd_prices = pd_prices.drop(columns=['flat_id'])

    print(pd_flats.head())
    print(pd_prices.head())

    pd_flats.to_sql('flats', con=conn, if_exists='replace', index=False)
    pd_prices.to_sql('prices', con=conn, if_exists='replace', index=False)

    c.execute("SELECT * FROM flats")
    list_flats = c.fetchone()
    print(list_flats)

    query_f = '''
                CREATE TABLE flats_copy(
                flat_id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                ad_id TEXT NOT NULL, 
                title TEXT,
                date_posted TEXT NOT NULL,
                date_scraped TEXT NOT NULL,
                location TEXT NOT NULL,
                seller TEXT,
                property_type TEXT,
                num_rooms integer,
                num_bathrooms integer,
                flat_area integer NOT NULL,
                text TEXT,
                description TEXT,
                photos_links TEXT,
                page_address TEXT
                );
            '''
        
    c.execute(query_f)
    c.execute('''insert into 
    flats_copy(flat_id, ad_id, title, date_posted, date_scraped, location, seller, property_type, num_rooms, num_bathrooms, flat_area, text, description, photos_links, page_address ) 
    select flat_id, ad_id, title, date_posted, date_scraped, location, seller, property_type, num_rooms, num_bathrooms, flat_area, text, description, photos_links, page_address from flats''')
    c.execute('drop table flats')
    c.execute('alter table flats_copy rename to flats')
    conn.commit()

    query_p = """
    CREATE TABLE prices_copy(
        price_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        flat_id INTEGER NOT NULL,
        price INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(flat_id) REFERENCES flats(flat_id) 
        );
    """
    c.execute(query_p)
    c.execute('''insert into 
                    prices_copy(price_id, flat_id, price, date ) 
                    select price_id, flat_id, price, date from prices''')
    c.execute('drop table prices')
    c.execute('alter table prices_copy rename to prices')
    conn.commit()

    conn.close()


def change_dates_flats_table():
    try:
        conn = sqlite3.connect('../data/flats.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise Exception

    cursor.execute("SELECT ad_id, date_posted, date_scraped FROM flats_new")
    list_flats = cursor.fetchall()

    for elem in list_flats:
        print(elem)

        ad_id = elem[0]
        date_posted = change_date_str(elem[1])
        date_scraped = change_date_str(elem[2])

        print(ad_id, date_posted, date_scraped)

        cursor.execute(f"UPDATE flats_new "
                       f"SET date_posted = \'{date_posted}\', "
                       f"date_scraped = \'{date_scraped}\' "
                       f'WHERE ad_id = {ad_id}')
        conn.commit()

    conn.close()


if __name__ == '__main__':
    change_id_longer()
