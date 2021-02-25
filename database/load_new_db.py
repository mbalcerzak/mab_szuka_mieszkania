import sqlite3


def change_date_str(text: str) -> str:
    if "/" in text:
        dd,mm,yyyy = text.split('/')
        return f"{yyyy}-{mm}-{dd}"
    else:
        return text


def load_new_db():
    try:
        conn = sqlite3.connect('../data/flats.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise Exception

    cursor.execute("SELECT ad_id, price, price_history, date_scraped FROM flats")
    list_flats = cursor.fetchall()

    for elem in list_flats:
        ad_id = elem[0]
        price = elem[1]
        price_history = eval(elem[2])
        date_scraped = elem[3]

        if date_scraped not in price_history:
            price_history[date_scraped] = price

        elif price_history[date_scraped] != price:
            date = change_date_str(date_scraped)
            cursor.execute(f"INSERT INTO prices VALUES("
                           "NULL, "
                           f"{ad_id}, "
                           f"{value}, "
                           f"\'{date}\' "
                           ")")
            conn.commit()

        for key, value in price_history.items():
            date = change_date_str(key)
            cursor.execute(f"INSERT INTO prices VALUES("
                           "NULL, "
                           f"{ad_id}, "
                           f"{value}, "
                           f"\'{date}\' "
                           ")")
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
    change_dates_flats_table()
