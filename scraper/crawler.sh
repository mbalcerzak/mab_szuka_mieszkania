# Run hourly

source /home/pi/Documents/mab_szuka_mieszkania/.venv/bin/activate

cd /home/pi/Documents/mab_szuka_mieszkania/scraper

python3 -m scrapy runspider crawler.py
