from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#things to add:
#add user input for item, automate to search for it and grab url, display current price
#ask to save item to database

url = "https://www.amazon.ca/PlayStation-4-Dual-Charging-Dock/dp/B00ENFVJJO/ref=sr_1_10?crid=2FQ1OYX6BS5AJ&keywords=playstation+4&qid=1642393254&sprefix=play%2Caps%2C136&sr=8-10"
#url = "https://www.amazon.ca/Gusseted-Quilted-Pillow-Hypo-Allergenic/dp/B01N4WAERJ/ref=sr_1_5?crid=3CIGG4PDDSD81&keywords=pillow&qid=1642535283&sprefix=pillow%2Caps%2C131&sr=8-5"
item = "PlayStation 4 Dual Charging Dock"

driver = webdriver.Chrome()
driver.get(url)

#price = (driver.find_element_by_xpath('//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]')).text
#price = driver.find_element_by_id("corePrice_desktop").text
price = driver.find_element_by_id("corePrice_feature_div").text
driver.close()

if price.find('\n') != -1:
    price_split = price.split('\n')
    price = price_split[0] + '.' + price_split[1]


print(price)



