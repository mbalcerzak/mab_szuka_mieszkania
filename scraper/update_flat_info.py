from utils import today_str


def update_price(cursor, ad_id, ad_price, conn):
    today = today_str()

    cursor.execute(f"SELECT flat_id FROM flats WHERE ad_id = '{ad_id}'")
    flat_id = cursor.fetchone()

    cursor.execute(f"INSERT INTO prices VALUES("
                   "NULL, "
                   f"{flat_id[0]}, "
                   f"{ad_price}, "
                   f"\'{today}\' "
                   ")")
    conn.commit()
