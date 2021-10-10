from utils import today_str


def update_price(cursor, ad_id, ad_price, conn):
    today = today_str()
    cursor.execute(f"INSERT INTO prices VALUES("
                   "NULL, "
                   f"{ad_id}, "
                   f"{ad_price}, "
                   f"\'{today}\' "
                   ")")
    conn.commit()
