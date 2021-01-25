import logging
import webbrowser
import scrapy
import sqlite3
import re

from scraping_gumtree import add_flat
from update_flat_info import check_if_row_exists, check_if_price_changed, update_price
from utils import get_ad_price, get_page_address,info_scraped_today, get_next_page, get_page_info

logging.getLogger('scrapy').setLevel(logging.WARNING)

# TODO change the db design -> 2 tables: flats, price


class BlogSpider(scrapy.Spider):
    name = "gumtree"
    start_urls = [
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/warszawa/mieszkanie/v1c9073l3200008a1dwp1?df=ownr&priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/praga-poludnie/mieszkanie/v1c9073l3200015a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/praga-polnoc/mieszkanie/v1c9073l3200014a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/wola/mieszkanie/v1c9073l3200025a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/srodmiescie/mieszkanie/v1c9073l3200017a1dwp1?priceType=FIXED',
        
    ]
    # webbrowser.open(start_urls[0])

    def parse(self, response):
        i = 1

        try:
            conn = sqlite3.connect('../data/flats.db')
            # conn = sqlite3.connect(r'C:\Users\kkql180\NonWorkProjects\mab_szuka_mieszkania\data\flats_test.db')
            cursor = conn.cursor()
        except sqlite3.Error as e:
            raise Exception

        for flat_ad in response.css('div.tileV1'):
            print("\n" + "-"*100 + " " + str(i))

            page_address = get_page_address(flat_ad)
            ad_price = get_ad_price(flat_ad)
            ad_id = page_address.split('/')[-1][3:12]

            if check_if_row_exists(cursor, ad_id):
                if check_if_price_changed(cursor, ad_id, ad_price):
                    update_price(cursor, ad_id, ad_price)
            else:
                add_flat(page_address, cursor)

            conn.commit()
            i += 1

        try:
            next_page = get_next_page(response)
            get_page_info(next_page)
            conn.close()

            if next_page is not None:
                yield response.follow(next_page, self.parse)

        except KeyError:
            info_scraped_today(cursor)
            print("I think we reached our 50 pages. KeyError occurred.")
