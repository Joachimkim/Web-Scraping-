#inoder to run the script in the virtual environment one has to 
# a) pip install scrapy
# b) pip install request
# c) pip install progress
# d) pip install pandas

import scrapy
import json
import time
import pandas as pd

start = time.time()

with open("url_data.json", encoding='utf-8') as data:
    data_ = json.load(data)
    list_urls = json.loads(data_)
    crypto_urls = list_urls['slugs']
    # print(type(crypto_urls))

class CryptoURLS(scrapy.Spider):
    name = 'crypto_urls_spider'
    start_urls = crypto_urls
    output = "scrapy_cryptos_urls.csv"
    coins = []

    def __init__(self):
        open(self.output, "w").close()
        
    def parse(self, response):
        crypto_body = response.css("body")
        COINS = dict()
        
        OFFICIAL_NAME = ".//div[@class='mr-md-3 tw-pl-2 md:tw-mb-0 tw-text-xl tw-font-bold tw-mb-0']/text()"
        OFFICIAL_URL = ".//div[@class='tw-flex flex-wrap tw-font-normal']"
        
        COINS["NAME (SYMBOL)"] = str(crypto_body.xpath(OFFICIAL_NAME).get()).strip('\n')
        COINS["OFFICIAL WEBSITE"] = crypto_body.xpath(OFFICIAL_URL).css('a::attr(href)').getall()[0]
        
        self.coins.append((COINS["NAME (SYMBOL)"], COINS["OFFICIAL WEBSITE"]))
        # print(COINS["NAME (SYMBOL)"], COINS["OFFICIAL WEBSITE"])
        
        # Write to file (changes)
        HEADERS = ["NAME (SYMBOL)", "OFFICIAL WEBSITE"]
        coins_dataframe = pd.DataFrame(self.coins, columns=HEADERS)
        coins_dataframe.to_csv(self.output)

        # yield print(COINS)

End = time.time()
ellapsedtime = (End - start)
print(ellapsedtime)