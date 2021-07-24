#########################################################################
# Script to add data from SQL DB to Grocy
#########################################################################

import requests
import os
import mysql.connector
from dotenv import load_dotenv
import json

load_dotenv()

mydb = mysql.connector.connect(
  host=os.getenv('MYSQL_HOST'),
  user=os.getenv('MYSQL_USERNAME'),
  password=os.getenv('MYSQL_PASSWORD'),
  database=os.getenv('MYSQL_DATABASE')
)
mycursor = mydb.cursor()

mycursor.execute('SELECT * FROM products')
myresult = list(mycursor.fetchall())

API_ENDPOINT = os.getenv('GROCY_API_ENDPOINT')

API_KEY = os.getenv('GROCY_API_KEY')

headers = {'GROCY-API-KEY':API_KEY, 'Accept': 'application/json'}

all_grocy_data_request = requests.get(url = API_ENDPOINT + "objects/product_barcodes", headers = headers)
all_grocy_data = all_grocy_data_request.json()

all_ean_codes = []
# Loop trough all_grocy_data and get all ean codes
for product in all_grocy_data:
  all_ean_codes.append(str(product['barcode']))

for data in myresult:
    # check if barcode exists in all_ean_codes
    if data[1] in all_ean_codes:
        continue

    print('Found one that doesnt exist' + data[2])

    body_1 = {
        "name" : data[2],
        "location_id": 4,
        "shopping_location_id": 1,
        "default_best_before_days": 7,
        "qu_id_purchase": 7,
        "qu_id_stock": 7,
        "qu_factor_purchase_to_stock": 1
    }

    r = requests.post(url = API_ENDPOINT + "objects/products", headers = headers, json = body_1)

    product_id = r.json()['created_object_id']

    body_2 = {"picnicean" : data[0]}

    r = requests.put(url = API_ENDPOINT + "userfields/products/" + str(product_id), headers = headers, json = body_2)

    body_3 = {
        "product_id" : product_id,
        "barcode" : data[1],
        "shopping_location_id": 1,
        "last_price" : data[4]
    }

    r = requests.post(url = API_ENDPOINT + "objects/product_barcodes", headers = headers, json = body_3)
