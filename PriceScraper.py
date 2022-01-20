from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import mysql.connector

# currently a script to webscrape information such as price and ratings for various items on Amazon
# Using Selenium for Python to go to the URL of the item on Amazon and use various web elements 
# to scrape item data
# store the findings in a database
# Can use results to see price changes at certain times for purposes such as buying at lower prices
# or to identify trends in price changes (such as price increase/decrease during holidays)
#
# may create a similar project with menu/user input as shown in commented out menu and function example of delete request
#
#Improvements
#   -Method of identifying price and such doesn't work for all items, so do a try and catch
#   and incorporate multiple methods of identifying web page elements
#   -Incorporate batch script to let this run on its own at certain times
#   -Send alerts for price changes 
#   -Pandas library to analyze data (maybe include this to the part 2 of this project with user menu)



# helper functions to call such as deleting logs of an item no longer being tracked

def delete_item(cursor):
    cursor.execute("SHOW TABLES" )
    show = cursor.fetchall()
    i = 1
    for x in show:
        print(x)

    print("Here is the list of items currently being tracked.")
    print("Please input the name of the item you want to delete from the database or press q to go back to the main menu:")
    choice = input()

    if choice == 'q':
        return
    else:
        cursor.execute("DROP TABLE " + choice)

# add urls to the list to track more items
# remove urls to stop tracking item (still in database if table isn't deleted)

url_list = [
'https://www.amazon.ca/PlayStation-4-Dual-Charging-Dock/dp/B00ENFVJJO/ref=sr_1_10?crid=2FQ1OYX6BS5AJ&keywords=playstation+4&qid=1642393254&sprefix=play%2Caps%2C136&sr=8-10',
'https://www.amazon.ca/Gusseted-Quilted-Pillow-Hypo-Allergenic/dp/B01N4WAERJ/ref=sr_1_5?crid=3CIGG4PDDSD81&keywords=pillow&qid=1642535283&sprefix=pillow%2Caps%2C131&sr=8-5',
'https://www.amazon.ca/GreenWorks-2600502-20-Inch-Corded-Thrower/dp/B00YYPR9F6/ref=sr_1_14?crid=2HWC994KOHRD2&keywords=snow%2Bblower&qid=1642664267&sprefix=snow%2Bblower%2Caps%2C262&sr=8-14&th=1'
]

# connect to my 'scraper' database in MySQL where it holds scraped data for the items I'm tracking

scraper_db = mysql.connector.connect(
    host = "localhost",
    user = "Scraper",
    password = "Pythonscraper",
    database = "scraper"
)

print("Successfully connected")

cursor = scraper_db.cursor()

# menu example 
# print("1. Run scraper for all items in database")
# print("2. Add new item to scrape")
# print("3. View item logs")
# print("4. Delete logs for an item you no longer want to track")

# choice = input()

# if choice = '4':
#     delete_item(cursor)


# method to scrape using Selenium

def scrape_item(url, cursor):
    driver = webdriver.Chrome()
    driver.get(url)

    # find title of the product which will be name of the table to track its data
    item = driver.find_element_by_id("productTitle").text

    # replace characters that are not allowed in table names in MySQL
    item = item.replace(' ', '_')                           
    item = item.replace('(', '_')
    item = item.replace(')', '_')
    item = item.replace('-', '_')

    # if item name is too long for table name, just use first 60 chars
    if len(item) > 60:
        item = item[0:60]
    
    # check if first char in item string is a number or not 
    if item[0].isdigit():
        item = '_' + item
    
    
    # scrape the price, rating and number of ratings of the item being tracked
    price = driver.find_element_by_id("corePrice_feature_div").text
    rating = driver.find_element_by_id("acrPopover").get_attribute("title")
    num_of_ratings = driver.find_element_by_id("acrCustomerReviewText").text

    driver.close()

    # format the scraped data and additional data into proper strings
    if price.find('\n') != -1:
        price_split = price.split('\n')
        price = price_split[0] + '.' + price_split[1]

    rating_split = rating.split(" ")
    rating = rating_split[0] + "/5"

    num_ratings_split = num_of_ratings.split(" ")
    num_of_ratings = num_ratings_split[0]

    run_date = datetime.now()
    run_date = run_date.strftime('%m/%d/%Y')


    # create table in database if it doesn't exist to start tracking for the item (ie new url)
    # table name is item name
    # table tracks the URL, price, rating, number of ratings and the date it was scraped
    cursor.execute('CREATE TABLE IF NOT EXISTS ' 
    + item + 
    ' (URL VARCHAR(255), Price VARCHAR(25), Rating VARCHAR(25), NumOfRatings VARCHAR(10), Date VARCHAR(25))')


    # insert query for inserting scraped data into table ie saving results to database
    insert_query = 'INSERT INTO ' + item + ' (URL, Price, Rating, NumOfRatings, Date) VALUES (%s, %s, %s, %s, %s)'
    insert_values = (url, price, rating, num_of_ratings, run_date)

    # execute insert
    cursor.execute(insert_query, insert_values)
    scraper_db.commit()


    # show current logs for an item or comment out to not show logs everytime script is ran
    print('Log data for ' + item + ':')
    cursor.execute("SELECT Price, Rating, NumOfRatings, Date FROM " + '`' + item +'`')
    select_item = cursor.fetchall()                     # list

    for x in select_item:
        print(x)


# scrape for all URLs in the URL list, adjust if scraping for specific items in list
for x in url_list:
    scrape_item(x, cursor)


#close cursor and connection
cursor.close()
scraper_db.close()
