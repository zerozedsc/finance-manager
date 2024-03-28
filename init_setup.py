from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, abort
from database.firebase_db import *
from database.local_db import *
from configs.config import *

app = Flask(__name__)
app.secret_key = 'zerozed'

create_logs("app", "app", "App started", status='info')

INFO_LEVEL = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']
TRANSACTIONS_TYPE = ['Daily Spending', 'Non-Daily Spending', 'Bills', 'Scholarship', 'Travel', 'Subscription']
FORM_TYPE = ["new-transaction"]

# navbar data
NAVBAR = {"transaction": [k for k in TRANSACTIONS_TYPE], }

# start collecting require data from firebase
# check local_db.json
with app.app_context():
    LOCAL_DATA = check_localdb()

    if CLOUD_SAVE and FIREBASE_DB_USE:
        if not LOCAL_DATA:
            fb2local()
        else:
            try:
                check_fb_latest = get_data("CONFIG", doc_id="CHECK", gettype="field", field_name="LAST_CHECK")
                if compare_datetime(check_fb_latest, LOCAL_DATA['_local']['check']['last_check']):
                    fb2local()
                    create_logs("local-data-update", "app", "Local data updated", status='info')
                else:
                    for updatedCollection in LOCAL_DATA['_local']['check']['updated_collections']:
                        pass

            except Exception as e:
                create_logs("local-data-update", "app", f"Local data update failed: {e}", status='error')

app.jinja_env.filters['fromjson'] = from_json
app.jinja_env.filters['gettype'] = get_type
