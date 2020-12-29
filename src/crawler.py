import scrapy
from lxml import html


class BlogSpider(scrapy.Spider):
    name = 'gumtree'
    start_urls = [
        'https://www.gumtree.pl/s-mieszkania-i-domy-sprzedam-i-kupie/warszawa/mieszkanie/v1c9073l3200008a1dwp1',
    ]

    def parse(self, response):
        for flat in response.css('div.tileV1'):
            yield {
                'page_address': flat.css('a::attr("href")').get()
            }

        next_page = response.css('a.arrows.icon-right-arrow.icon-angle-right-gray').attrib["href"]

        if str(next_page)[-1] == '4':
            exit()

        print(f"NEXT PAGE: {next_page}")
        if next_page is not None:
            yield response.follow(next_page, self.parse)
