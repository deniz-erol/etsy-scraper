import urllib.request
from bs4 import BeautifulSoup

ProductList = []  # List to store name of the product
PriceList = []    # List to store price of the product
Links = []        # List to store product image links

#Goes to Etsy product page and scrape data
print('Give me a Etsy product link')
URL = input()

page = urllib.request.urlopen(URL)
soup = BeautifulSoup(page.read(), "html.parser")

name = soup.find('h1', class_='wt-text-body-03 wt-line-height-tight wt-break-word wt-mb-xs-1').text.strip()
price = soup.find('p', class_='wt-text-title-03 wt-mr-xs-2').text.strip()
pimage = soup.find('img', class_='wt-max-width-full wt-horizontal-center wt-vertical-center carousel-image wt-rounded')
image = str(pimage["data-src-zoom-image"])

# Connect to the database

import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='UID',
                             password='PW',
                             database='DB-name',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
# Insert into MySQL table
with connection:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `scrape_table` (`name`, `price`, `image`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, price, image))
        
    connection.commit()
    print('Data insert complete!')

# Print last input

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `scrape_table` ORDER BY `product_id` DESC LIMIT 1"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)

