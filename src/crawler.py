import logging
import scrapy
import webbrowser
from datetime import date

from scraping_gumtree import get_flat_info, add_flat

logging.getLogger('scrapy').setLevel(logging.WARNING)


class BlogSpider(scrapy.Spider):

    name = 'gumtree'
    start_urls = [
        # 'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/warszawa/mieszkanie/v1c9073l3200008a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/warszawa/mieszkanie/v1c9073l3200008a1dwp1?df=ownr&priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/praga-poludnie/mieszkanie/v1c9073l3200015a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/praga-polnoc/mieszkanie/v1c9073l3200014a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/wola/mieszkanie/v1c9073l3200025a1dwp1?priceType=FIXED',
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/srodmiescie/mieszkanie/v1c9073l3200017a1dwp1?priceType=FIXED'
    ]
    webbrowser.open(start_urls[0])

    def parse(self, response):
        i = 1
        for flat in response.css('div.tileV1'):
            print("\n")
            print("-"*100 + " " + str(i))
            page_address = flat.css('a::attr("href")').get()
            yield {
                'page_address': page_address,
                'date': date.today()
            }
            flat = get_flat_info(page_address)
            add_flat(flat, update=False)
            i += 1

        try:
            next_page = response.css('a.arrows.icon-right-arrow.icon-angle-right-gray').attrib['href']
            if next_page is not None:
                print(f"\n   (   NEXT PAGE: {next_page}   )")
                yield response.follow(next_page, self.parse)

        except KeyError as ke:
            print("I think we reached our 50 pages. KeyError occurred.")
