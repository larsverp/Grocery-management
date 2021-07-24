#########################################################################
# Script used by the scanner above the bin. (Used when trowing items away)
#########################################################################

import drivers
import requests
from time import sleep

load_dotenv()

display = drivers.Lcd()

API_ENDPOINT = os.getenv('GROCY_API_ENDPOINT')
API_KEY = os.getenv('GROCY_API_KEY')
headers = {'GROCY-API-KEY':API_KEY, 'Accept': 'application/json'}

display.lcd_clear()
display.lcd_display_string("Fetching API..", 1)

all_grocy_ean_request = requests.get(url = API_ENDPOINT + "objects/product_barcodes", headers = headers)
all_grocy_ean = all_grocy_ean_request.json()

all_ean_codes = {}
for product in all_grocy_ean:
  all_ean_codes[str(product['barcode'])] = product['product_id']

all_grocy_products_request = requests.get(url = API_ENDPOINT + "objects/products", headers = headers)
all_grocy_products = all_grocy_products_request.json()

all_products = {}
for product in all_grocy_products:
    all_products[product['id']] = {
        'name' : product['name'],
        'picnic_id' : product['userfields']['picnicean'],
        'quick_consume_amount' : product['quick_consume_amount']
    }

display.lcd_clear()
display.lcd_display_string("Done", 1)
display.lcd_display_string("Starting up", 2)
sleep(5)

while True:
    display.lcd_clear()
    display.lcd_display_string("Scan product:", 1)

    try:
        barcode = input()
        display.lcd_clear()

        display.lcd_display_string(str(all_products[all_ean_codes[str(barcode)]]['name'])[:15], 1)
        stock_body = {
            'amount' : all_products[all_ean_codes[str(barcode)]]['quick_consume_amount']
        }
        stock_minus_one = requests.post(url = API_ENDPOINT + "stock/products/" + str(all_ean_codes[str(barcode)]) + "/consume", headers = headers, json = stock_body)
        if stock_minus_one.status_code == 200:
            display.lcd_display_string("Succes -" + str(all_products[all_ean_codes[str(barcode)]]['quick_consume_amount']), 2)
            sleep(5)
        else:
            display.lcd_display_string("Grocy error", 2)
            sleep(5)
    except:
        display.lcd_clear()
        display.lcd_display_string("ERROR", 1)
        sleep(5)
