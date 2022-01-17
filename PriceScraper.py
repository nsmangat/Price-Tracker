from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "https://www.amazon.ca/"
# browser = webdriver.Chrome(executable_path = "C:\Users\nsman\Desktop\Amazon Price Scraper")
# browser = webdriver.Chrome()
# browser.get(url)
#driver = webdriver.Chrome(executable_path = 'C:\Users\nsman\Desktop\Amazon Price Scraper')

getSearch = input("Please type in an item ")

driver = webdriver.Chrome()
driver.get(url)


search = driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]')
search.clear()
search.send_keys(getSearch)
search.submit()


driver.close()


