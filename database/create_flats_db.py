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

    # sql_create_flats_table = """CREATE TABLE IF NOT EXISTS flats(
    #                                 ad_id integer PRIMARY KEY,
    #                                 title text NOT NULL,
    #                                 date_posted text NOT NULL,
    #                                 date_scraped text NOT NULL,
    #                                 location text NOT NULL,
    #                                 price integer,
    #                                 seller text,
    #                                 property_type text,
    #                                 num_rooms integer,
    #                                 num_bathrooms integer,
    #                                 flat_area integer,
    #                                 parking text,
    #                                 description text,
    #                                 photos_links text,
    #                                 price_history text,
    #                                 page_address text);
    #                             """

    # sql_create_flats_table = """CREATE TABLE IF NOT EXISTS flats(
    #                                 ad_id integer PRIMARY KEY,
    #                                 title text NOT NULL,
    #                                 date_posted text NOT NULL,
    #                                 date_scraped text NOT NULL,
    #                                 location text NOT NULL,
    #                                 seller text,
    #                                 property_type text,
    #                                 num_rooms integer,
    #                                 num_bathrooms integer,
    #                                 flat_area integer,
    #                                 parking text,
    #                                 description text,
    #                                 photos_links text,
    #                                 page_address text);
    #                             """

    sql_create_flats_new_dsgn = """CREATE TABLE flats_new as SELECT  
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

    sql_create_price_changes_table= """CREATE TABLE IF NOT EXISTS prices(
                                            price_id integer PRIMARY KEY AUTOINCREMENT,
                                            flat_id integer NOT NULL,
                                            price integer,
                                            date text,
                                            FOREIGN KEY(flat_id) REFERENCES flats_new(ad_id))   
                                     """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_flats_new_dsgn)
        create_table(conn, sql_create_price_changes_table)
        print("Created!")
    else:
        print("Error! Cannot create the database connection")


if __name__ == '__main__':
    create_database()
