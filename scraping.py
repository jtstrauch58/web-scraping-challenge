from bs4 import BeautifulSoup
import requests
import pymongo


# Setup connection to mongodb
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Select database and collection to use
db = client.store_inventory
produce = db.produce


url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify())