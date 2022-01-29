import json
import sqlite3
from datetime import date


def query_latest_price(cursor):
    json_prices = {}

    query = """SELECT
                    max(price_id) AS max_id,
                    ad_id,
                    price
                FROM
                    prices
                    LEFT JOIN flats ON flats.flat_id = prices.flat_id
                GROUP BY
                    ad_id
            """

    cursor.execute(query)
    latest_prices = cursor.fetchall()

    for row in latest_prices:
        flat_id = str(row[1])
        price = row[2]

        json_prices[flat_id] = price

    today = date.today().strftime("%Y-%m-%d")
    json_prices['date'] = today

    return json_prices



def get_latest_prices_json():
    with open('../data/latest_prices.json', 'r') as f:
        latest_prices = json.load(f)

    return latest_prices


def create_price_json():
    try:
        conn = sqlite3.connect('../data/flats.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise Exception

    latest_prices = query_latest_price(cursor)

    with open('../data/latest_prices.json', 'w') as f:
        json.dump(latest_prices, f)

    conn.close()


if __name__ == "__main__":
    create_price_json()
