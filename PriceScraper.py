from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import mysql.connector

#username: Scraper
#password: Pythonscraper

#things to add:
#add user input for item, automate to search for it and grab url, display current price
#ask to save item to database

url = "https://www.amazon.ca/PlayStation-4-Dual-Charging-Dock/dp/B00ENFVJJO/ref=sr_1_10?crid=2FQ1OYX6BS5AJ&keywords=playstation+4&qid=1642393254&sprefix=play%2Caps%2C136&sr=8-10"
#url = "https://www.amazon.ca/Gusseted-Quilted-Pillow-Hypo-Allergenic/dp/B01N4WAERJ/ref=sr_1_5?crid=3CIGG4PDDSD81&keywords=pillow&qid=1642535283&sprefix=pillow%2Caps%2C131&sr=8-5"
length = len(url)
scraper_db = mysql.connector.connect(
    host = "localhost",
    user = "Scraper",
    password = "Pythonscraper",
    database = "scraper"
)

cursor = scraper_db.cursor()


driver = webdriver.Chrome()
driver.get(url)


item = driver.find_element_by_id("productTitle").text

price = driver.find_element_by_id("corePrice_feature_div").text
rating = driver.find_element_by_id("acrPopover").get_attribute("title")
num_of_ratings = driver.find_element_by_id("acrCustomerReviewText").text

driver.close()

if price.find('\n') != -1:
    price_split = price.split('\n')
    price = price_split[0] + '.' + price_split[1]

rating_split = rating.split(" ")
rating = rating_split[0] + "/5"

#run_date = date.today()
run_date = datetime.now()
run_date = run_date.strftime('%m/%d/%Y')

num_ratings_split = num_of_ratings.split(" ")
num_of_ratings = num_ratings_split[0]

print(length)
print(run_date)
print(item)
print(price)
print(rating)
print(num_of_ratings)
print('the rating is ' + item)

#insert query for inserting item data into table

insert_query = 'INSERT INTO ' + '`' + item +'`' + ' (URL, Price, Rating, NumOfRatings, Date) VALUES (%s, %s, %s, %s, %s)'
insert_values = (url, price, rating, num_of_ratings, run_date)


#create table in database to start tracking for the item 
cursor.execute('CREATE TABLE IF NOT EXISTS ' 
+ '`' + item + '`' + 
' (URL VARCHAR(255), Price VARCHAR(25), Rating VARCHAR(25), NumOfRatings VARCHAR(10), Date VARCHAR(25))')

cursor.execute(insert_query, insert_values)
scraper_db.commit()

cursor.execute("SELECT * FROM " + '`' + item +'`')
select_item = cursor.fetchall()

for x in select_item:
    print(x)

cursor.close()
scraper_db.close()



