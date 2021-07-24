#########################################################################
# Script used to add the delivered Picnic prodcts
# !!! Retrieving the last order is not possible so please add to cart using the app !!!
#########################################################################

import os
import json
import requests
import mysql.connector
from dotenv import load_dotenv
from python_picnic_api import PicnicAPI

load_dotenv()

mydb = mysql.connector.connect(
  host=os.getenv('MYSQL_HOST'),
  user=os.getenv('MYSQL_USERNAME'),
  password=os.getenv('MYSQL_PASSWORD'),
  database=os.getenv('MYSQL_DATABASE')
)
mycursor = mydb.cursor()

picnic = PicnicAPI(username=os.getenv('PICNIC_USERNAME'), password=os.getenv('PICNIC_PASSWORD'), country_code='NL')
picnic_order = picnic.get_cart()['items']

API_ENDPOINT = os.getenv('GROCY_API_ENDPOINT')
API_KEY = os.getenv('GROCY_API_KEY')
headers = {'GROCY-API-KEY':API_KEY, 'Accept': 'application/json'}

all_grocy_data_request = requests.get(url = API_ENDPOINT + "objects/product_barcodes", headers = headers)
all_grocy_data = all_grocy_data_request.json()

all_ean_codes = {}
for product in all_grocy_data:
  all_ean_codes[str(product['barcode'])] = product['product_id']

for item in picnic_order:
    stock_body = {
        "amount" : item['items'][0]['decorators'][0]['quantity']
    }
    mycursor.execute('SELECT ean_code FROM products WHERE picnic_id = ' + item['items'][0]['id'])
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        if myresult[0][0] in all_ean_codes:
            stock_plus_one = requests.post(url = API_ENDPOINT + "stock/products/" + str(all_ean_codes[myresult[0][0]]) + "/add", headers = headers, json = stock_body)
            if stock_plus_one.status_code == 200:
                print("Succesfully added product to Grocy")
    else:
        try_again = True
        while try_again == True:
            new_product_ean = input("Please scan " + item['items'][0]['name'] + ": ")
            if new_product_ean in all_ean_codes:
                os.system('cls||clear')
                print('This ean code already belongs to product with id: ')
                print(all_ean_codes[new_product_ean])
                print('Try again...')
            else:
                try_again = False

                sql = 'INSERT INTO products (picnic_id, ean_code, description, quantity, price) VALUES (%s, %s, %s, %s, %s)'
                val = (item['items'][0]['id'], new_product_ean, item['items'][0]['name'], item['items'][0]['unit_quantity'], item['items'][0]['price'])
                mycursor.execute(sql, val)
                mydb.commit()
                print('Added ' + item['items'][0]['name'] + ' to products table')

                try:
                    body_1 = {
                    "name" : item['items'][0]['name'],
                    "location_id": 4,
                    "shopping_location_id": 1,
                    "default_best_before_days": 7,
                    "qu_id_purchase": 7,
                    "qu_id_stock": 7,
                    "qu_factor_purchase_to_stock": 1
                    }

                    r = requests.post(url = API_ENDPOINT + "objects/products", headers = headers, json = body_1)

                    product_id = r.json()['created_object_id']

                    all_ean_codes[new_product_ean] = product_id

                    body_2 = {"picnicean" :item['items'][0]['id']}

                    r = requests.put(url = API_ENDPOINT + "userfields/products/" + str(product_id), headers = headers, json = body_2)

                    body_3 = {
                        "product_id" : product_id,
                        "barcode" : new_product_ean,
                        "shopping_location_id": 1,
                    }

                    r = requests.post(url = API_ENDPOINT + "objects/product_barcodes", headers = headers, json = body_3)

                    stock_plus_one = requests.post(url = API_ENDPOINT + "stock/products/" + str(product_id) + "/add", headers = headers, json = stock_body)
                    if stock_plus_one.status_code == 200:
                        print("Succesfully added product to Grocy")
                except:
                    print("Something went wrong, the name probably already exists for product: " +  item['items'][0]['name'])
