from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#things to add:
#add user input for item, automate to search for it and grab url, display current price
#ask to save item to database

url = "https://www.amazon.ca/PlayStation-4-Dual-Charging-Dock/dp/B00ENFVJJO/ref=sr_1_10?crid=2FQ1OYX6BS5AJ&keywords=playstation+4&qid=1642393254&sprefix=play%2Caps%2C136&sr=8-10"
item = "PlayStation 4 Dual Charging Dock"

driver = webdriver.Chrome()
driver.get(url)

price = (driver.find_element_by_xpath('//*[@id="corePrice_desktop"]/div/table/tbody/tr/td[2]/span[1]/span[2]')).text

driver.close()

print(price)



