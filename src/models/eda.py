import sqlite3



def main():
    try:
        conn = sqlite3.connect('../data/flats.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise Exception

    cursor.execute(f'SELECT * FROM flats where price_history')
    return True if len(cursor.fetchall()) != 0 else False



if __name__ == "__main__":
    main()