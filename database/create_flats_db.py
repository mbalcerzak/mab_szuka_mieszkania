import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def create_database():
    database = '..//data//flats.db'

    flats_table = """CREATE TABLE flats_new as SELECT  
                        ad_id,
                        title,
                        date_posted,
                        date_scraped,
                        location,
                        seller,
                        property_type,
                        num_rooms,
                        num_bathrooms,
                        flat_area,
                        parking text,
                        description,
                        photos_links,
                        page_address FROM flats"""

    prices_table = """CREATE TABLE prices(
                        price_id integer PRIMARY KEY AUTOINCREMENT,
                        flat_id integer NOT NULL,
                        price integer,
                        date text,
                        FOREIGN KEY(flat_id) REFERENCES flats_new(ad_id))"""

    taken_down = """CREATE TABLE taken_down(
                        event_id integer PRIMARY KEY AUTOINCREMENT,
                        flat_id integer NOT NULL,
                        date text,
                        active text, 
                        FOREIGN KEY(flat_id) REFERENCES flats(ad_id))"""

    conn = create_connection(database)

    if conn is not None:
        # create_table(conn, flats_table)
        # create_table(conn, prices_table)
        create_table(conn, taken_down)
        print("Created!")
    else:
        print("Error! Cannot create the database connection")


if __name__ == '__main__':
    pass
