from flask import Flask, render_template, redirect, url_for, request
from database.firebase_db import *
from configs.config import *

app = Flask(__name__)

create_logs("app", "app", "App started", status='info')


@app.route("/")
def home():
    page_title = "Main Dashboard"
    front_data = {"title": [MAIN_TITLE, page_title], }  # this dictionary is for frontend data (title, name, etc...)
    value_content = {
        "currency": CURRENCY}  # this dictionary is mainly focus on content that have value (total, price, etc, ...)

    return render_template('index.html', front_data=front_data, value=value_content)


@app.route('/form/<form_type>', methods=['GET', 'POST'])
def form(form_type):
    timestamp_id = timestampID()
    page_title = "[Form] " + " ".join(form_type.split("-")).title()
    front_data = {"title": [MAIN_TITLE, page_title, "form",
                            form_type], }  # this dictionary is for frontend data (title, name, etc...)
    value_content = {
        "currency": CURRENCY}  # this dictionary is mainly focus on content that have value (total, price, etc, ...)

    if form_type == "new-transaction":
        item_data = {
            'shop_name': "",
            'type': "",
            'cash_source': "",
            'date': "",
            'item_name': "",
            'brand_name': "",
            'category': "",
            'quantity': "",
            'metric_unit': "",
            'price': "",
            'tax': "",
        }

        tags = [" ".join(tag.split("_")) for tag in item_data.keys()]

        if request.method == "POST":
            # Process form data here
            item_data['type'] = request.form['transaction_type']
            item_data['shop_name'] = request.form['shop_name']
            item_data['date'] = request.form['date']
            item_data['cash_source'] = request.form['cash_source']
            submit_transaction = str(request.form['submit_transaction']).split(";")
            print(submit_transaction)
            transactions = []
            for item in submit_transaction:
                if len(item) > 1:
                    item_tag = item.split(",")
                    c = 0
                    for tag in item_data.keys():
                        if tag not in ['type', 'shop_name', 'date', 'cash_source']:
                            item_data[tag] = numeric(item_tag[c])
                            c += 1
                    transactions.append(item_data.copy())

            pprint(transactions, indent=4)

            return redirect(url_for('form', form_type='new-transaction'))

        return render_template('form.html', data_tags=tags,
                               front_data=front_data, value=value_content)

    return render_template('form.html', front_data=front_data, content=value_content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
