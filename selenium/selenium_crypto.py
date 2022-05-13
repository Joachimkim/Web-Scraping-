#inoder to run the script in the virtual environment one has to 
# a) pip install selenium
# b) pip install request
# c) pip install progress
# d) pip install pandas

import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from progress.bar import ChargingBar
import json


start = time.time()

# Fixing Minor Warnings Incase you experience any
from selenium.webdriver.chrome.options import Options

# Fixing some minor Chrome errors and OS errors
options = Options()

# options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument('--ignore-ssl-errors')
options.add_argument('log-level=3')

# Initializing the driver
driver = webdriver.Chrome(options=options)
base_url = "https://www.coingecko.com"

crypto_urls = []
crypto_data_list = list()
official_websites = list()

# Implicitly wait
def web_wait_time():
    return driver.implicitly_wait(5)

# Sleep
def web_sleep_time(seconds):
    return time.sleep(seconds)

# web_wait_time()

# Our 
def main():
    driver.get(base_url)
    data = driver.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    web_elements = []
    
    bar = ChargingBar('*** Scraping Data *** :', max=100)
    for data_elements in data:
        web_elements.append(data_elements.text.split("\n"))
        bar.next()
        
        SLUG = data_elements.find_element(By.XPATH, ".//a[@class='d-lg-none font-bold tw-w-12']").get_attribute('href')
        crypto_urls.append(SLUG)

    bar.finish()
    print("--- Done Scraping Data---", end="\n")
    # print(web_elements)
    # web_sleep_time(10)
    
    for element in web_elements:
        RANK = element[0]
        NAME = element[1]
        SYMBOL = element[2]
        PRICE = element[-1].split(" ")[0]
        MARKET_CAP = element[-1].split(" ")[]
        
        crypto_data_list.append((RANK, NAME, SYMBOL, PRICE, MARKET_CAP))
    print("--- Done Updating ---", end="\n")
              
def write_main_to_file():
    try:
        crypto_dataframe = pd.DataFrame(crypto_data_list, columns=["RANK", "NAME", "SYMBOL", "PRICE", "MARKET_CAP"])
        crypto_dataframe.to_csv("crypto_data_selenium.csv")
        print("--- Successfully Created CSV File ---")
    except Exception as e:
        print("Error: ", e)


def create_url_json():
    slug_dict = {"urls": crypto_urls}
    json_urls = json.dumps(slug_dict)
    with open('url_data_selenium.json', 'w+', encoding='utf-8') as file:
        json.dump(json_urls, file, ensure_ascii=False, indent=4)
    print("--- Done Creating JSON File ---")



def get_official_urls():
    bar = ChargingBar('*** Scraping Official URLS *** :', max=100)
    for url in crypto_urls:
        driver.get(url)
        bar.next()
        
        official_name = driver.find_element(By.XPATH, ".//div[@class='mr-md-3 tw-pl-2 md:tw-mb-0 tw-text-xl tw-font-bold tw-mb-0']").text
        official_urls = driver.find_element(By.XPATH, './/div[@class="tw-flex flex-wrap tw-font-normal"]').find_elements(By.TAG_NAME, "a")

        temp_urls = list()
        for o_url in official_urls:
            url = o_url.get_attribute('href').split("\n")
            temp_urls.append(url)
            
            
        official_url = temp_urls[0][0]
        official_websites.append((official_name, official_url))
          
    bar.finish()
    print("--- Done Scraping URLS ---", end="\n")


def write_official_urls_to_file():
    try:
        urls_dataframe = pd.DataFrame(official_websites, columns=["NAME (SYMBOL)", "OFFICIAL WEBSITE"])
        urls_dataframe.to_csv("crypto_urls_selenium.csv")
        print("--- Successfully Created CSV File ---")
    except Exception as e:
        print("Error: ", e)         
    
        # print(official_name, official_urls)

main()
write_main_to_file()
# web_wait_time()

# Incase of JSON Data --> API
create_url_json()

# web_sleep_time(30)

get_official_urls()
print(len(official_websites))
write_official_urls_to_file()

End = time.time()
ellapsedtime = (End - start)
print(ellapsedtime)

# End Session
driver.quit()

