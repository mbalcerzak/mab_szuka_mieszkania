import logging
import scrapy
import sqlite3

from scraping_gumtree import add_flat
from update_flat_info import update_price
from utils import get_ad_price, get_page_address, info_scraped_today, get_next_page, get_page_info, get_ad_id, get_flat_id_from_ad
from latest_prices import get_latest_prices_json

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class BlogSpider(scrapy.Spider):
    name = "gumtree"
    start_urls = [
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/warszawa/mieszkanie/v1c9073l3200008a1dwp1?df=ownr&priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/praga-poludnie/mieszkanie/v1c9073l3200015a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/praga-polnoc/mieszkanie/v1c9073l3200014a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/wola/mieszkanie/v1c9073l3200025a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/ochota/mieszkanie/v1c9073l3200013a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/srodmiescie/mieszkanie/v1c9073l3200017a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/mokotow/mieszkanie/v1c9073l3200012a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/bemowo/mieszkanie/v1c9073l3200009a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/targowek/mieszkanie/v1c9073l3200018a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/zoliborz/mieszkanie/v1c9073l3200026a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/wilanow/mieszkanie/v1c9073l3200023a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/ursynow/mieszkanie/v1c9073l3200020a1dwp1?priceType=FIXED'
    ]

    def parse(self, response):
        i = 1

        try:
            conn = sqlite3.connect('../data/flats.db')
            cursor = conn.cursor()
        except sqlite3.Error as e:
            raise Exception

        latest_prices = get_latest_prices_json()

        for flat_ad in response.css('div.tileV1'):
            print("\n" + "-"*100 + " " + str(i))

            page_address = get_page_address(flat_ad)
            ad_price = get_ad_price(flat_ad)
            ad_id = get_ad_id(page_address)

            if ad_id in latest_prices:
                if int(latest_prices[ad_id]) != int(ad_price):
                    print(f"{latest_prices[ad_id]} --> {ad_price}")
                    update_price(cursor, ad_id, ad_price, conn)
                else:
                    print(f"{ad_id} exists in the database. Price is still the same")
            else:
                add_flat(page_address, cursor, conn)

            i += 1

        try:
            next_page = get_next_page(response)
            get_page_info(next_page)
            conn.close()

            if next_page is not None:
                yield response.follow(next_page, self.parse)

        except KeyError:
            print(info_scraped_today(cursor))
            print("I think we reached our 50 pages. KeyError occurred.")
