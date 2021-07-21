# Easy inventorying tool for Picnic users

**Disclaimer: This project is absolutely not meant to be a very pretty piece of code. This is only used for connecting ean code's to picnic id's**

Picnic sadly doesn't use ean code's in their app. So with this 'easy' tool I add all my items from my order in my basket and start scanning everything that is not yet known with a cheap barcode scanner. It's not ideal, but especialy the 'hunting mode' is very nice to use.

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
