import sqlite3
from datetime import datetime


def close_db():
    try:
        conn = sqlite3.connect('data/flats.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise Exception
    conn.close()


def check_if_row_exists(cursor, ad_id):
    cursor.execute(f'SELECT ad_id FROM flats WHERE ad_id = "{ad_id}"')
    try:
        ad_id = cursor.fetchone()[0]
        print(f"Ad {ad_id} found in the database.")
        return True
    except TypeError:
        print(f"{ad_id} not found in the database.")
        return False


def check_if_price_changed(cursor, ad_id, ad_price):
    cursor.execute(f'SELECT price FROM flats WHERE ad_id = "{ad_id}"')
    old_price = int(cursor.fetchone()[0])
    if old_price != int(ad_price):
        print("Price has changed")
        return True
    else:
        print("Price is still the same.")
        return False


def update_price(cursor, ad_id, ad_price):
    cursor.execute(f'SELECT price_history FROM flats '
                   f'WHERE ad_id = "{ad_id}"')
    price_history = eval(cursor.fetchone()[0])

    cursor.execute(f'SELECT date_scraped FROM flats '
                   f'WHERE ad_id = "{ad_id}"')
    previous_date = cursor.fetchone()[0]

    cursor.execute(f'SELECT price FROM flats '
                   f'WHERE ad_id = "{ad_id}"')
    old_price = int(cursor.fetchone()[0])
    new_price = int(ad_price)
    today = datetime.today().strftime('%d/%m/%Y')

    if str(previous_date) not in price_history:
        price_history[previous_date] = old_price

    if str(today) not in price_history:
        price_history[today] = new_price

    cursor.execute(f"UPDATE flats "
                   f"SET price_history = \"{price_history}\", "
                   f"    price = {new_price}, "
                   f"    date_scraped = \'{today}\'"
                   f'WHERE ad_id = "{ad_id}"')

    print(f"PRICE updated: {price_history}")
