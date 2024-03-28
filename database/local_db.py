from configs.config import *


def db_structure():
    data = {'_local': {
        "collections": [
            "CASH_SOURCE",
            "SHOPS",
            "TRANSACTION",
            "USER"
        ],
        "check": {
            "last_update": datetime_now(),
            "last_check": datetime_now(),
            "latest": True,
            "updated_collections": [],
            "history": []
        }
    }}

    for k in data['_local']['collections']:
        data[k] = {}

    return data


def check_localdb():
    try:
        with open('database/local_db.json', 'r', encoding='utf-8') as file:
            create_logs("local-data-load", "app", "Local data loaded", status='info')
            return json.load(file)
    except FileNotFoundError:
        with open('database/local_db.json', 'w', encoding='utf-8') as file:
            json.dump({}, file, indent=4, ensure_ascii=False)
            create_logs("local-data-load", "app", "Local data created", status='warning')
        return False


def local_save_all(data):
    '''Save all local data to Firebase'''
    local_db_path = "database/local_db.json"
    try:
        with open(local_db_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        create_logs("local-save", "local_json", "Local data saved when exit", status='info')
    except Exception as e:
        create_logs("local-save", "local_json", f"Failed to save local data when exit: {e}", status='error')


def save_local_backup(data, filepath):
    '''Save local data to a backup file'''
    try:
        with open(filepath, encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        create_logs("local-backup", "local_json", "Local data saved to backup", status='info')
    except Exception as e:
        create_logs("local-backup", "local_json", f"Failed to save local data to backup: {e}", status='error')


def save_test_local(data, filepath):
    '''Save local data to a test file'''
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        create_logs("local-backup", "local_json", "Local data saved to backup", status='info')
    except Exception as e:
        create_logs("local-backup", "local_json", f"Failed to save local data to backup: {e}", status='error')
