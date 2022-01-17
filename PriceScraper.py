from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "https://www.amazon.ca/"
# browser = webdriver.Chrome(executable_path = "C:\Users\nsman\Desktop\Amazon Price Scraper")
# browser = webdriver.Chrome()
# browser.get(url)
#driver = webdriver.Chrome(executable_path = 'C:\Users\nsman\Desktop\Amazon Price Scraper')

#getSearch = input("Please type in an item ")
get_search = "toaster"

driver = webdriver.Chrome()
driver.get(url)


search = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
search.clear()
search.send_keys(get_search)
search.submit()

# price_list = driver.find_elements_by_xpath('//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[6]/div/span/div/div/div[2]/div[3]/div/a/span/span[1]')
item_prices = driver.find_elements_by_class_name('a-price')

#price_list = driver.find_element_by_class_name('a-offscreen')
#price_list = driver.find_element_by_css_selector('#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.sg-row > div.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span:nth-child(4) > div.s-main-slot.s-result-list.s-search-results.sg-row > div:nth-child(12) > div > span > div > div > div:nth-child(3) > div.a-section.a-spacing-none.a-spacing-top-small.s-price-instructions-style > div > a > span > span.a-offscreen')
# price_list.text

price_list = []

# for x in range(len(price_list)):
#     price_list.

for price in item_prices:
    price_list.append(price.text)

print(*price_list)

driver.close()


