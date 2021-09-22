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

items_on_shopping_list_request = requests.get(url = API_ENDPOINT + "objects/shopping_list", headers = headers)
items_on_shopping_list = items_on_shopping_list_request.json()


for item in items_on_shopping_list:
    item__data_request = requests.get(url = API_ENDPOINT + "objects/products/"+str(item['product_id']), headers = headers)
    item_data = item__data_request.json()

    if item_data['userfields']['picnicean'] != None and item['done'] != 1:
        picnic.add_product(item_data['userfields']['picnicean'], item['amount'])
        update_item_on_shoppinglist = requests.put(url = API_ENDPOINT + "objects/shopping_list/" + str(item['id']) , headers = headers, json={'done' : 1})
        print('Added ' + item_data['name'])
