from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "https://www.amazon.ca/"
# browser = webdriver.Chrome(executable_path = "C:\Users\nsman\Desktop\Amazon Price Scraper")
# browser = webdriver.Chrome()
# browser.get(url)

driver = webdriver.Chrome()
driver.get(url)

getSearch = input("Please type in an item ")


driver.close()

#check
