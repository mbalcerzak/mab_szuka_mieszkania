from utils import today_str


def update_price(cursor, ad_id: str, ad_price: int, conn) -> None:
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
