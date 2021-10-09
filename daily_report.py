'''
An email goes out each morning with the following info:
    - how many new ads were added
    - how many price changes has been detected
    - number of ads in total
'''
import smtplib
import ssl
import sqlite3
from datetime import datetime

from scraper.utils import info_scraped_today
from passwords import gmail_user


def main():
    gmail_login, gmail_password = gmail_user()

    today = datetime.today().strftime('%d %B %Y')

    try:
        conn = sqlite3.connect('data/flats.db')
        cursor = conn.cursor()
    except sqlite3.Error as e:
        raise Exception

    msg = (f"Subject: Scraper Report {today} \n\n {info_scraped_today(cursor)}")

    print(info_scraped_today(cursor))

    context = ssl.create_default_context()
    port = 587
    smtp_server = "smtp.gmail.com"

    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls(context=context)
    server.ehlo()
    server.login(gmail_login, gmail_password)
    server.sendmail(from_addr=gmail_login, to_addrs=gmail_login, msg=msg)
    server.close()


if __name__ == "__main__":
    main()
