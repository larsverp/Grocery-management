#########################################################################
# Script to add missing picnicean codes to Grocy by comparing cartdata
# !!! Noting smart, just compares positions, so 1th picnic product should be equal to first grocy product without picnic ean. !!!
#########################################################################

import os
import json
import requests
from dotenv import load_dotenv
from python_picnic_api import PicnicAPI

load_dotenv()

API_ENDPOINT = os.getenv('GROCY_API_ENDPOINT')
API_KEY = os.getenv('GROCY_API_KEY')
headers = {'GROCY-API-KEY':API_KEY, 'Accept': 'application/json'}

load_dotenv()

picnic = PicnicAPI(username=os.getenv('PICNIC_USERNAME'), password=os.getenv('PICNIC_PASSWORD'), country_code='NL')

cartData_raw = picnic.get_cart()
cartData = cartData_raw['items']

all_grocy_products_request = requests.get(url = API_ENDPOINT + "objects/products", headers = headers)
all_grocy_products = all_grocy_products_request.json()

all_grocy_products.sort(key=lambda x: x['name'], reverse=False)

picnicean_less_products = []
for product in all_grocy_products:
    if product['userfields']['picnicean'] == None:
        picnicean_less_products.append(product)

for product_num in range(0, len(cartData)):
    is_equal = input('Is ' + cartData[product_num]['items'][0]['name'] + ' the same product as ' + picnicean_less_products[product_num]['name'] + '? (y/n)')
    if is_equal == 'y':
        body = {"picnicean" : cartData[product_num]['items'][0]['id']}
        r = requests.put(url = API_ENDPOINT + "userfields/products/" + str(picnicean_less_products[product_num]['id']), headers = headers, json = body)
