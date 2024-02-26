from flask import Flask, render_template, redirect, url_for, request
from database.firebase_db import *

app = Flask(__name__)
MAIN_TITLE = "Finance Planner"


@app.route("/")
def home():
    page_title = "Main Dashboard"
    front_data = {"title": [MAIN_TITLE, page_title],}  # this dictionary is for frontend data (title, name, etc...)
    value_content = {}  # this dictionary is mainly focus on content that have value (total, price, etc, ...)
    collection_names = get_collection_names()
    for collection_name in collection_names:
        value_content[collection_name] = get_collection(collection_name)

    print (value_content)

    return render_template('index.html', front_data=front_data, value_content=value_content)


@app.route('/form/<form_type>', methods=['GET', 'POST'])
def form(form_type):

    page_title = "[Form] " + " ".join(form_type.split("-")).title()
    front_data = {"title": [MAIN_TITLE, page_title, "form" ,form_type],}  # this dictionary is for frontend data (title, name, etc...)
    value_content = {}  # this dictionary is mainly focus on content that have value (total, price, etc, ...)

    if form_type == "new-transaction":
        if request.method == "POST":
            # Process form data here
            type = request.form['type']
            shop_name = request.form['shop_name']
            items = []
            itemCount = 1  # Start counting items from 1
            while f'item_name_{itemCount}' in request.form:
                item_data = {
                    'shop_name': shop_name,
                    'type': type,
                    'category': request.form[f'category_{itemCount}'],
                    'date': request.form[f'date_{itemCount}'],
                    'item_name': request.form[f'item_name_{itemCount}'],
                    'quantity': request.form[f'quantity_{itemCount}'],
                    'unit_measurement': request.form[f'unit_measurement_{itemCount}'],
                    'item_price': request.form[f'item_price_{itemCount}'],
                    'tax': request.form[f'tax_{itemCount}'],
                }
                items.append(item_data)
                itemCount += 1

            print(items, itemCount)

            return redirect(url_for('form', form_type='new-transaction'))
        return render_template('form.html', front_data=front_data, content=value_content)

    return render_template('form.html', front_data=front_data, content=value_content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
