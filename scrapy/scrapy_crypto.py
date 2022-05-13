#inoder to run the script in the virtual environment one has to 
# a) pip install scrapy
# b) pip install request
# c) pip install progress
# d) pip install pandas

# Importing Necessary dependencies
import time
import scrapy
import csv
import json

start = time.time()

# Subclassing from scrapy Spider class
class CryptoScraper(scrapy.Spider):
    
    # Meta data - required for our subclassed scraper
    name = 'crypto_spider'
    start_urls = ["https://www.coingecko.com"] # Init URL
    
    # Later write to file
    output = "scrapy_currencies.csv"
    
    # We shall need the slug container for all the crypto coins
    crypto_slugs = []

    # Everytime our class is instantiated, it opens this file for read-write ops
    def __init__(self):
        open(self.output, "w").close()

    # Parse Method --subclassed from Spider with a response parameter
    def parse(self, response):
        # Get the response from the get_request(start_urls)
        crypto_body = response.css("tbody > tr")
        # print(crypto_body)
        coins_list = list()
        
        # Open our output file
        HEADERS = ["RANK", "NAME", "SYMBOL", "PRICE", "MARKET_CAP", "SLUG"]
        with open(self.output, "a+", newline="") as coin:
            writer = csv.DictWriter(coin, delimiter=',',fieldnames=HEADERS)
            writer.writeheader()
            # Basically looping through table rows under the body & finding where our data resides
            for crypto in crypto_body:
                RANK = ".//td[@class='table-number tw-text-left text-xs cg-sticky-col cg-sticky-second-col tw-max-w-14 lg:tw-w-14']/text()"
                NAME = './/a[@class="tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between"]/text()'
                SYMBOL = './/a[@class="d-lg-none font-bold tw-w-12"]/text()'
                PRICE = 'td > span ::text'
                MARKET_CAP = 'td > span ::text'
                SLUG = './/a/@href'

                COINS = dict()

                # Populate our empty dict with our scraped data
                COINS["RANK"] = str(crypto.xpath(RANK).get()).strip('\n')
                COINS["NAME"] = str(crypto.xpath(NAME).get()).strip('\n')
                COINS["SYMBOL"] = str(crypto.xpath(SYMBOL).get()).strip('\n')
                COINS["PRICE"] = crypto.css(PRICE).getall()[0]
                COINS["MARKET_CAP"] = crypto.css(MARKET_CAP).getall()[5]
                COINS["SLUG"] = crypto.xpath(SLUG).getall()[0]
                
                coins_list.append(COINS)
                
                # Getting all crypto_urls from the slugs for further scraping
                self.crypto_slugs.append(str(self.start_urls[0] + COINS["SLUG"]).strip('\n'))
                
                # Dump to json & write to a file
                slug_dict = {"slugs": self.crypto_slugs}
                json_urls = json.dumps(slug_dict)
                with open('url_data.json', 'w+', encoding='utf-8') as file:
                    json.dump(json_urls, file, ensure_ascii=False, indent=4)
                
                # Finally write the main data to a CSV File too
                
                writer.writerow(COINS)
                yield print(COINS)

End = time.time()
ellapsedtime = (End - start)
print(ellapsedtime)
