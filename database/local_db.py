from configs.config import *


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
