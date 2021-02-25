import sqlite3
import pandas as pd


def create_dataframes(path_db, output_path):
    """Load SQLite tables into pickle format"""
    con = sqlite3.connect(path_db)

    df_flats = pd.read_sql_query("SELECT * FROM flats", con)
    df_prices_all = pd.read_sql_query("SELECT * FROM prices", con)
    # choose the lastest price of each flat
    df_prices_latest = pd.read_sql_query("SELECT max(price_id), flat_id, price, date FROM prices GROUP BY flat_id", con)

    df_flats.to_pickle(f"{output_path}/flats.pkl")
    df_prices_all.to_pickle(f"{output_path}/prices_all.pkl")
    df_prices_latest.to_pickle(f"{output_path}/prices_latest.pkl")


if __name__ == "__main__":
    create_dataframes('../data/flats.db', '../data')
