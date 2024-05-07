# Finance Manager Changelog

## 7-5-2024
#### - **_TODO_** focus on cash source page (bank, cash hand, etc..)
* **Create a page to show all account**
* **Create a page to add new account**
* **Create a page to edit account**
* **Create a page to delete account**
* **Create a page to show all transaction based on account**
#### - **_FIXED_** bug in `config.py` where function `from_json` not returning dict because of flask.jsonify
* **Change `flask.jsonify` to `json.loads`**
#### - **_ADDED_** cash source panel `cash_source.py`, with dropdown navbar to choose cash source type 



## 2-5-2024
#### - **_ADDED_** into `script.html` to show toast
#### - **_DONE_** `daily-table.html` to show the total of transaction
* **Add Spend Type**
* **Table creation done (for each input, spending type, year, month and day)**
* **No problem with japanese letter**
#### - **_FIXED_** bug inside `local_db.json` which code inside `app.py` wrongly saving the data
* **Spending type not being save in correct place**
#### - **_TODO_** sorting the table based on the user requirements and searching algorithm
* **Sorting according to the data header**
* **Searching algorithm to find the data based on the user input**
#### - **_TODO-FIX_** `app.py` and `navbar.html` toast not working properly


## 1-5-2024
#### - **_ADJUSTED_** `daily-table.html` to show the total of transaction
* **Right now only for input panel (year, month, date) and shows total Daily Transaction**
* **Not doing anything to table**
#### - **_TODO_** `daily-table.html`
* **Create a table that can show item based on the requirements (day, month, year, transaction type, etc..)**
* **Need to solve Japanese letter problem**

## 28-3-2024
#### - **_CREATED_** `local_db.py` to handle all local database operations
#### - **_CREATED_** `requirements.txt` file to list all python dependencies
#### - **_PUSHED_** to GitHub with tag local-db
#### - **_REPLACED_** mainly some of code inside `init_setup.py`
* **Creating variable to check using cloud database or not**
* **Did some adjustment on init setup saving data from firebase to local**
#### - **_PUSHED_** to GitHub with tag init-setup adjustment

## 27-3-2024
#### - _**DONE**_ new-transactions form page
#### - _**PUSHED**_ to GitHub with tag new-transactions-form


