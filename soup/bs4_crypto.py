#inoder to run the script in the virtual environment one has to 
# a) pip install beautifulsoup4
# b) pip install request
# c) pip install progress
# d) pip install lxml

# Importing Necessary dependencies

from bs4 import BeautifulSoup 
import requests
import csv
import time
import pandas as pd
from progress.bar import ChargingBar

start = time.time()

# HTTP headers let the client and the server pass additional information with an HTTP request or response. 
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
 Chrome/86.0.4240.75 Safari/537.36'}


# Let's catch the error while creating our get session on main URL
try:
    base_url = "https://www.coingecko.com"
    #Getting response and decoding the actual HTML content
    response = requests.get(base_url, headers=headers).content.decode()
    # print(response)
except Exception as e:
    # Any error that arises can be captured here
    print("Error ", e)
 
# Let's create a  of our soup to parse the HTML for operations using  "lxml"    
soup = BeautifulSoup(response, "lxml")
# Get our information by inspecting Coin Gecko
table_body = soup.find("tbody").findAll('tr')
# print(len(table_body))

# Create some global containers for our scraped content
crypto_coins = []
crypto_slugs = []
COINS = dict([])

# An empty CSV File will be used to dump the scraped data;
MAIN_OUTPUT_CSV = "crypto_currencies.csv"

# Help us control server requests and from being banned or flagged while scraping
def wait(seconds):
    return time.sleep(seconds)

# Our Main Function that will return most useful data for analysis
def main():
    for row in table_body:
        # Getting Slugs of the different cryptos
        slugs = row.find(class_="d-lg-none font-bold tw-w-12").get("href")
        # print("Slugs ", slugs)
        crypto_slugs.append(slugs)
        # print(row)
        
        # Let's wait for 5 seconds
        # wait(5)
        
        # Now let's scrape to find the data we need using bs4
        try:
            rank = row.find(class_="table-number tw-text-left text-xs cg-sticky-col cg-sticky-second-col tw-max-w-14 lg:tw-w-14")
            name = row.find(class_="tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between")
            symbol =  row.find(class_="d-lg-none font-bold tw-w-12")
            price = row.find(class_="td-price price text-right pl-0")
            market_cap = row.find(class_="td-market_cap cap col-market cap-price text-right")
            # print(rank, name, symbol, price, market_cap)
            
            
            # Get actual text that we need & update our COINS dict()
            COINS["RANK"] = rank.get_text()
            COINS["NAME"] = name.get_text()
            COINS["SYMBOL"] = symbol.get_text()
            COINS["PRICE"] = price.get_text()
            COINS["MARKET_CAP"] = market_cap.get_text()
            # print(COINS)
            crypto_coins.append((COINS["RANK"], COINS["NAME"], COINS["SYMBOL"], COINS["PRICE"], COINS["MARKET_CAP"]))
            
        except Exception as e:
            # pass
            print("Error ", e)

def write_main_to_file():
    # Open the CSV file for writing
    HEADERS = ["RANK", "NAME", "SYMBOL", "PRICE", "MARKET_CAP"]
    
    coins_dataframe = pd.DataFrame(crypto_coins, columns=HEADERS)
    coins_dataframe.to_csv(MAIN_OUTPUT_CSV)
    
    print(f"--- Successfully created {MAIN_OUTPUT_CSV} file ---")
        
# Scraping slugs that we shall later use to create URLS    
crypto_urls = list()
def create_urls():
    for slug in crypto_slugs:
        url = base_url + slug
        crypto_urls.append(url)
    # print(crypto_urls)    
    print("--- Successfully created URLS ---")
    
# Now let's create those URLS and write them to a file too;
crypto_urls_list = list()
def scrape_urls():
    bar = ChargingBar('*** Scraping Crypto URLS *** :', max=100)
    for idx , url in enumerate(crypto_urls):
        crypto_session = requests.get(url, headers=headers)
        crypto_content = crypto_session.content.decode()
        # print(crypto_content)
        
        # Creating the soup
        soup = BeautifulSoup(crypto_content, "html.parser")
        
        # Identifying our information class;
        official_name = soup.find(class_ = "mr-md-3 tw-pl-2 md:tw-mb-0 tw-text-xl tw-font-bold tw-mb-0")
        official_urls = soup.find(class_ = "tw-flex flex-wrap tw-font-normal").find("a")
        
        # Get the real data
        official_name = official_name.get_text().strip("\n")
        official_urls = official_urls.get("href")
        # print(official_name, official_urls)
        
        # Append to the official crypto_urls storage
        crypto_urls_list.append((official_name, official_urls))
        bar.next()
        # print(f"*** scraping crypto link number {idx} ..... Hold--On ***")
    print("\n")
    print("--- Done scraping all urls and appending them ---", end="\n")
    bar.finish()
        
CRYPTO_URLS_CSV = "crypto_urls.csv"
def write_urls_to_file():
    # Open the CSV file for writing
    HEADERS = ["NAME (symbol)", "OFFICIAL WEBSITE"]
    
    coins_dataframe = pd.DataFrame(crypto_urls_list, columns=HEADERS)
    coins_dataframe.to_csv(CRYPTO_URLS_CSV)
    
    
    
    # Write to an excel file for later use;
    # with open(CRYPTO_URLS_CSV, "a+", newline="", encoding="utf-8") as crypto_url:
    #     writer = csv.writer(crypto_url)
        
    #     for data in crypto_urls_list:
    #         writer.writerows([data])
    print(f"--- Successfully created {CRYPTO_URLS_CSV} file ---")
    
    
# Running our scraper
main()  
write_main_to_file()

# Wait for a minute
# wait(60)

# Get all the URLS 
create_urls()
scrape_urls()
write_urls_to_file()

End = time.time()
ellapsedtime = (End - start)
print(ellapsedtime)