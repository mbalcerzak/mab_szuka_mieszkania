import logging
import scrapy
import sqlite3
import json
from datetime import date

from scraping_gumtree import add_flat
from update_flat_info import update_price
from utils import get_ad_price, get_page_address, info_scraped_today, get_next_page, get_page_info, get_ad_id
from latest_prices import get_latest_prices_json

logging.getLogger('scrapy').setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class BlogSpider(scrapy.Spider):
    name = "gumtree"

    with open('../start_urls.json', 'r') as f:
        start_urls = json.load(f)

    def parse(self, response):
        i = 1

        report = {'new': 0, 'existing': 0, 'change': 0}

        try:
            conn = sqlite3.connect('../data/flats.db')
            cursor = conn.cursor()
        except sqlite3.Error as e:
            raise Exception

        latest_prices = get_latest_prices_json()
        today = date.today().strftime("%Y-%m-%d")
        
        if latest_prices['date'] != today:
            raise Exception("Update 'latest price JSON' ")

        for flat_ad in response.css('div.tileV1'):
            page_address = get_page_address(flat_ad)
            ad_price = get_ad_price(flat_ad)
            ad_id = get_ad_id(page_address)

            if ad_id in latest_prices:
                try:
                    if int(latest_prices[ad_id]) != int(ad_price):
                        update_price(cursor, ad_id, ad_price, conn)
                        report['change'] += 1
                    else:
                        report['existing'] += 1
                except ValueError:
                    print(f"Wrongly put price: {ad_price}")
            else:
                add_flat(page_address, cursor, conn)
                report['new'] += 1

            i += 1

        for tp, n in report.items():
            print(f"{tp}: {n}")

        try:
            next_page = get_next_page(response)
            get_page_info(next_page)
            conn.close()

            if next_page is not None:
                yield response.follow(next_page, self.parse)

        except KeyError:
            print(info_scraped_today(cursor))
            print("We reached our 50 pages")
