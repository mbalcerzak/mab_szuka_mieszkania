import sqlite3
from builtins import eval


def connection():
    try:
        conn = sqlite3.connect('../data/flats.db')
    except sqlite3.Error as e:
        raise Exception

    return conn


def get_price_history(c) -> list:
    c.execute('SELECT count(*) FROM flats WHERE price_history != \'{}\'')
    print(f"There are {c.fetchone()[0]} ads for which the price has changed")

    c.execute('SELECT price, price_history FROM flats WHERE price_history != \'{}\'')
    return c.fetchall()


def main():
    c = connection().cursor()
    price_history_list = get_price_history(c)
    print(price_history_list)

    for elem in price_history_list:
        current_price = elem[0]
        price_history = eval(elem[1])
        date_posted = min(price_history)
        original_price = price_history[date_posted]

        print(price_history, current_price)

        for date, price_change in price_history.items():
            if date != date_posted:
                difference = round((int(price_change) - int(original_price))/int(original_price), 4) * 100
                print(f"{date}| {original_price} -> {price_change} | {difference:.2f} %")
            elif price_change != current_price:
                difference = round((int(current_price) - int(original_price)) / int(original_price), 4) * 100
                print(f"{date}| {original_price} -> {current_price} | {difference:.2f} %")

        print("-" * 40)


if __name__ == "__main__":
    main()
