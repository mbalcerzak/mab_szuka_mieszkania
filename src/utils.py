import re
from datetime import datetime


def info_scraped_today(cursor):
    """Print how many ads were scraped today and how many there are in the whole database"""
    today = datetime.today().strftime('%d/%m/%Y')
    cursor.execute(f"SELECT count(*) FROM flats WHERE date_scraped = '{today}'")
    ads_today = cursor.fetchone()[0]

    cursor.execute(f"SELECT count(*) FROM flats")
    all_ads = cursor.fetchone()[0]

    print(f"Today we managed to scrape: {ads_today} new ads. \n Overall: {all_ads}")


def get_ad_price(flat):
    price = flat.css('span.ad-price::text').get()
    price = re.sub("[^\d\.,]", "", price)
    return price


def get_page_address(flat):
    address = flat.css('a::attr("href")').get()
    address = f'https://www.gumtree.pl{address}'
    return address


def get_page_info(next_page: str) -> None:
    """Print page number and which district we are scraping now"""
    page = re.findall(r"page-\d+", next_page)[0]
    page_num = page.split('-')[-1]
    district = next_page.split('/')[2].upper()

    print(f"\n\n{' '*15}({district} | NEXT PAGE: {page_num}){' '*15}\n")


def get_next_page(response):
    next_page = response.css('a.arrows.icon-right-arrow.icon-angle-right-gray').attrib['href']
    return next_page