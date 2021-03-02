import sqlite3
import requests
from bs4 import BeautifulSoup

from scraper.scraping_gumtree import get_price
from scraper.update_flat_info import check_if_row_exists, check_if_price_changed, \
    update_price


def get_flat_ad_price(page_address):
    page = requests.get(page_address)
    soup = BeautifulSoup(page.content, 'html.parser')
    return get_price(soup)


def check_ad_valid(page_address):
    page = requests.get(page_address)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup.find('div', class_="message")


def main():
    """
    A script to run through all the ads and see if any of the prices changed
    Also checks if the ad is still hanging
    """
    try:
        conn = sqlite3.connect('../data/flats.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise Exception

    # TODO too slow
    cursor.execute(f'SELECT ad_id, page_address FROM flats')
    flat_list = cursor.fetchall()

    for flat in flat_list:
        ad_id, page_address = flat[0], flat[1]

        ad_price = get_flat_ad_price(page_address)
        if ad_price != 0:
            if check_if_row_exists(cursor, ad_id):
                if check_if_price_changed(cursor, ad_id, ad_price):
                    update_price(cursor, ad_id, ad_price, conn)
                    conn.commit()


if __name__ == "__main__":
    main()
