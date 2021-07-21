# Grocery management

## Setup Linux/Mac:
Create a venv using `python3 -m venv ./venv`

To activate the venv run `source venv/bin/activate`

Install the latests required packaged using `pip install -r requirements.txt`

## Setup Windows:
Install virtualenv using `pip install virtualenv`

Create a venv using `virtualenv --python C:\Path\To\Python\python.exe venv`

To activate the venv run `.\venv\Scripts\activate`

Install the latests required packaged using `pip install -r requirements.txt`

## Adding new packages:
When adding new packaged you should always update the requirements.txt file so the next developer can use this file to update their venv. You should use `pip freeze > requirements.txt` for convenience.
