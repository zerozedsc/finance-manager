from flask import Flask, render_template
from database.firebase_db import *

app = Flask(__name__)
MAIN_TITLE = "Finance Planner"


@app.route("/")
def home():
    page_title = "Main Dashboard"
    front_data = {"title": [MAIN_TITLE, page_title],
                  "page-hierarchy": ["0"]}  # this dictionary is for frontend data (title, name, etc...)
    value_content = {}  # this dictionary is mainly focus on content that have value (total, price, etc, ...)
    collection_names = get_collection_names()
    for collection_name in collection_names:
        value_content[collection_name] = get_collection(collection_name)

    print (value_content)

    return render_template('index.html', front_data=front_data, value_content=value_content)


@app.route('/form/<form_type>', methods=['GET', 'POST'])
def form(form_type):

    page_title = "[Form] " + " ".join(form_type.split("-")).title()
    front_data = {"title": [MAIN_TITLE, page_title],
                  "page-hierarchy": ["1"]}  # this dictionary is for frontend data (title, name, etc...)



    return render_template('form.html', front_data=front_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
