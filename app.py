import flask
from flask import Flask, render_template

app = Flask(__name__)
MAIN_TITLE = "Finance Planner"


@app.route("/")
def home():
    page_title = "Main Dashboard"
    front_data = {"title": [MAIN_TITLE, page_title],
                  "page-hierarchy": ["0"]}  # this dictionary is for frontend data (title, name, etc...)
    value_content = {}  # this dictionary is mainly focus on content that have value (total, price, etc, ...)

    return render_template('index.html', front_data=front_data, value_content=value_content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
