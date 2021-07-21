# Easy inventorying tool for Picnic users

**Disclaimer: This project is absolutely not meant to be a very pretty piece of code. This is only used for connecting ean code's to picnic id's. And it works. Also I'm in no way related to Picnic.**

Picnic sadly doesn't use ean code's in their app. So with this 'easy' tool I add all my items from my order in my basket and start scanning everything that is not yet known with a cheap barcode scanner. It's not ideal, but especialy the 'hunting mode' is very nice to use.

## Setup the DB:
I'm using a MySQL database, containing 1 table named `products` that contains 6 columns:

picnic_id | ean_code | description | quantity | price | jumbo_product
----------|----------|-------------|----------|-------|--------------
10467828  | 8715817023754 | Aubergine | 1 stuk |     55   |   NULL
90006124	| 8718868261359	|Bio pastinaken	| 400 gram	| 139 | NULL

The `jumbo_product` column is a bool that is  only set to 1 when the product is a Jumbo product (I order from both Picnic and Jumbo, but Jumbo just uses the ean code so no need to store a diferent code.)

## Setup Linux/Mac:
Create a venv using `python3 -m venv ./venv`

To activate the venv run `source venv/bin/activate`

Install the latests required packaged using `pip install -r requirements.txt`

rename .env.example to .env and fill in all the fields

## Setup Windows:
Install virtualenv using `pip install virtualenv`

Create a venv using `virtualenv --python C:\Path\To\Python\python.exe venv`

To activate the venv run `.\venv\Scripts\activate`

Install the latests required packaged using `pip install -r requirements.txt`

rename .env.example to .env and fill in all the fields

## Adding new packages:
When adding new packaged you should always update the requirements.txt file so the next developer can use this file to update their venv. You should use `pip freeze > requirements.txt` for convenience.

## How to use it:

### When you completed the above steps, just run the program using `python index.py`

#### The following questions will be asked:

##### Do you want to fetch the picnic shopping cart? (y/n)
This will fetch the Picnic API and save your current cart to a json file. This way you don't have to make a request to the Picnic API everytime, even when you stop the programm. When answering `n` it will assume the file is already present. So when running it for the first time: answer `y`

##### Do you want to search the Jumbo site as well? (y/n)
When enabled it will search on the Jumbo site for every product before asking you to select the product from your Picnic cart. WATCH OUT: When adding the product using the Jumbo product, you can't enter a Picnic id anymore. **You should only use this when the product you're scanning is not for sale in the Picnic app**

##### Do you want to enable picnic item hunt mode? (y/n)
**Only available when answering no on the Jumbo site question** This is my ✨Favorite mode✨ This mode will just ask you to scan a certain product, so when you own a wireless scanner like I do, this is a amazing way of adding the products to the DB. It's like a egg hunt, but for ean codes 🥚
