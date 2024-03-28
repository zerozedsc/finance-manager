from database.firebase_db import *
from database.local_db import *
from configs.config import *

create_logs("app", "app", "App started", status='info')

INFO_LEVEL = ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'light', 'dark']
TRANSACTIONS_TYPE = ['Daily Spending', 'Non-Daily Spending', 'Bills', 'Scholarship', 'Travel', 'Subscription']
FORM_TYPE = ["new-transaction"]

# navbar data
NAVBAR = {"transaction": [k for k in TRANSACTIONS_TYPE], }

# start collecting require data from local, if firebase true then check firebase data
with app.app_context():
    LOCAL_DATA = check_localdb()
    create_logs("local-data-load", "app", "Local data loaded", status='info')

    if LOCAL_DATA:
        create_logs("local-data-check", "app", "Local data exist", status='info')
    else:
        create_logs("local-data-check", "app", "Local data not exist", status='warning')

    if CLOUD_SAVE:
        if FIREBASE_DB_USE:
            # check firebase data
            create_logs("firebase-data-load", "app", "Firebase data check and loaded", status='info')
            if not LOCAL_DATA:
                LOCAL_DATA = fb2local()
            else:
                try:
                    check_fb_latest = get_data("CONFIG", doc_id="CHECK", gettype="field", field_name="LAST_CHECK")
                    if compare_datetime(check_fb_latest, LOCAL_DATA['_local']['check']['last_check']):
                        LOCAL_DATA = fb2local()
                        update_data("CONFIG", doc_id="CHECK", data={"LAST_CHECK": datetime_now()})
                        create_logs("local-data-update", "app", "Local data updated", status='info')
                    else:
                        for updatedCollection in LOCAL_DATA['_local']['check']['updated_collections']:
                            pass

                except Exception as e:
                    create_logs("local-data-update", "app", f"Local data update failed: {e}", status='error')

    elif not LOCAL_DATA and not CLOUD_SAVE:
        LOCAL_DATA = db_structure()
        create_logs("local-data-create", "app", "Local data created", status='warning')

    else:
        create_logs("cloud-save-check", "app", "Cloud save is off", status='warning')


app.jinja_env.filters['fromjson'] = from_json
app.jinja_env.filters['gettype'] = get_type
