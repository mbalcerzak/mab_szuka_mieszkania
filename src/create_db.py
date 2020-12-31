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


def db_path():
    return '../data/flats.db'


def main():
    database = db_path()

    sql_create_flats_table = """CREATE TABLE IF NOT EXISTS flats(
                                    ad_id integer PRIMARY KEY,
                                    date_added text NOT NULL,
                                    location text NOT NULL,
                                    price integer,
                                    seller text,
                                    property_type text,
                                    num_rooms integer,
                                    num_bathrooms integer,
                                    flat_area integer,
                                    parking text,
                                    description text,
                                    photos_links text );
                                """

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_flats_table)
        print("Created! Or it was already there...")
    else:
        print("Error! Cannot create the database connection")


if __name__ == '__main__':
    main()
