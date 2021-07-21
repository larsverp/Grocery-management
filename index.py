import os
import json
import mysql.connector
from dotenv import load_dotenv
from python_picnic_api import PicnicAPI
from supermarktconnector.jumbo import JumboConnector

load_dotenv()

mydb = mysql.connector.connect(
  host=os.getenv('MYSQL_HOST'),
  user=os.getenv('MYSQL_USERNAME'),
  password=os.getenv('MYSQL_PASSWORD'),
  database=os.getenv('MYSQL_DATABASE')
)
mycursor = mydb.cursor()

jumbo = JumboConnector()
picnic = PicnicAPI(username=os.getenv('PICNIC_USERNAME'), password=os.getenv('PICNIC_PASSWORD'), country_code="NL")

def list_items():
    os.system('cls||clear')
    for key in items_in_order:
        print(key + " : " + items_in_order[key]['name'])
    item_number = input("Please select item or type stop: ")
    if item_number != "stop":
        sql = "INSERT INTO products (picnic_id, ean_code, description, quantity, price) VALUES (%s, %s, %s, %s, %s)"
        val = (items_in_order[item_number]['id'], ean, items_in_order[item_number]['name'], items_in_order[item_number]['quantity'], items_in_order[item_number]['price'])
        mycursor.execute(sql, val)
        mydb.commit()
        del items_in_order[item_number]
        print("Item added to products table")

answer = input("Do you want to fetch the picnic shopping card? (y/n) ")
if answer == 'y':
    print("Fetching and saving shopping card...")
    file = open("cardData.json", "w", encoding='utf-8')
    file.write(json.dumps(picnic.get_cart(), ensure_ascii=False, indent=4))
    file.close()
    print("Shoping card is fetched and saved")

search_via_jumbo = input("Do you want to search the Jumbo site as well? (y/n) ")

f = open('cardData.json', 'r')
data = json.load(f)
items_in_order = {}
item_count = 0
for item in data['items']:
    mycursor.execute("SELECT description FROM products WHERE picnic_id = " + item['items'][0]['id'])
    myresult = mycursor.fetchall()
    if len(myresult) <= 0:
        items_in_order[str(item_count)] = {'id' :  item['items'][0]['id'], 'name' :  item['items'][0]['name'], 'quantity' :  item['items'][0]['unit_quantity'] , 'price' : item['items'][0]['price']}
        item_count += 1

while 0 != 1:
    ean = input("Please scan item or type exit:")
    if ean == "exit":
        break
    mycursor.execute("SELECT description FROM products WHERE ean_code = " + ean)
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        print("Item already exists")
        print(myresult[0])
    else:
        jumboResults = jumbo.search_products(query=ean, size=1, page=0)
        if len(jumboResults['products']['data']) > 0 and search_via_jumbo == 'y':
            print(jumboResults)
            print("Found item on Jumbo site:")
            print(jumboResults['products']['data'][0]['title'])
            add_jumbo_product = input("Do you want to add this product using the Jumbo data? (y/n) ")
            if add_jumbo_product == 'y':
                mycursor.execute("INSERT INTO products (ean_code, description, quantity, price, jumbo_product) VALUES (%s, %s, %s, %s, %s)", (ean, jumboResults['products']['data'][0]['title'], jumboResults['products']['data'][0]['quantity'], jumboResults['products']['data'][0]['prices']['price']['amount'], 1))
                mydb.commit()
                print("Item added to products table")
            else:
                list_items()
        else:
            list_items()
