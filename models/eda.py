import sqlite3


def connection():
    try:
        conn = sqlite3.connect('../data/flats.db')
    except sqlite3.Error as e:
        raise Exception

    return conn


def print_count():
    c = connection().cursor()

    for col in ['date_scraped', 'date_posted', 'location', 'num_rooms']:
        print(col.upper())

        c.execute(f"SELECT {col}, count({col}) as how_many FROM flats GROUP BY {col}")
        for elem in c.fetchall():
            print(f"{elem}")

        print("-"*80)

    c.execute(f"SELECT location, num_rooms, count(num_rooms) as how_many FROM flats GROUP BY location, num_rooms")
    print("LOCATION + NUM_ROOMS")
    for elem in c.fetchall():
        print(f"{elem}")

    print("-" * 80)

    c.execute(f"SELECT count(*) FROM flats")
    all_ads = c.fetchone()[0]
    print(f"Scraped overall: {all_ads} ads")


if __name__ == "__main__":
    print_count()
