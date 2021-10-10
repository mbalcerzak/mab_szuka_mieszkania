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
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise Exception

    pd_flats = pd.read_sql("SELECT * FROM flats", conn)
    pd_prices = pd.read_sql("SELECT * FROM prices", conn)

    with open('../data/id_dict.json', 'r') as f:
        ids_json = json.load(f)

    pd_flats["ad_id"] = pd_flats["ad_id"].apply(lambda x: ids_json[str(x)])
    pd_prices["flat_id"] = pd_prices["flat_id"].apply(lambda x: ids_json[str(x)])

    pd_flats.to_sql('flats', con=conn, if_exists='replace', index=False)
    pd_prices.to_sql('prices', con=conn, if_exists='replace', index=False)

    cursor.execute("SELECT * FROM flats")
    list_flats = cursor.fetchone()[0]
    print(list_flats)

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
    # change_dates_flats_table()
    change_id_longer()
    # write_dict_ids()
