import scrapy

from scraping_gumtree import get_flat_info, add_flat
from datetime import date


class BlogSpider(scrapy.Spider):

    name = 'gumtree'
    start_urls = [
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/warszawa/mieszkanie/v1c9073l3200008a1dwp1?priceType=FIXED'
    ]

    def parse(self, response):
        i = 0
        for flat in response.css('div.tileV1'):
            page_address = flat.css('a::attr("href")').get()
            yield {
                'page_address': page_address,
                'date': date.today()
            }

            flat = get_flat_info(page_address)
            add_flat(flat)

            if i == 5:
                exit()
            i += 1

        # next_page = response.css('a.arrows.icon-right-arrow.icon-angle-right-gray').attrib["href"]
        #
        # if 'dwp2' in str(next_page):
        #     exit()
        #
        # print(f"NEXT PAGE: {next_page}")
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
