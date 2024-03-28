from firebase_admin import credentials, firestore
from configs.config import *
import firebase_admin

# Initialize Firebase Admin SDK
cred = credentials.Certificate('creds/firebase_cred.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


# firestore functions
def get_collection_names():
    global db
    """Retrieve all collection names from the Firestore database."""
    collections = db.collections()
    return [collection.id for collection in collections]


def add_data(collection_name, doc_id, add_type="collection", field_name="", data=""):
    global db, LOCAL_DATA

    """Add a new document to the Firestore database."""
    try:
        collection = LOCAL_DATA["_local"]["collections"]
        if collection_name not in collection:
            collection.append(collection_name)
            LOCAL_DATA["_local"]["collections"] = collection
            with open('local_db.json', 'w') as file:
                json.dump(LOCAL_DATA, file, indent=4)
            current_app.logger.info(f"Collection '{collection_name}' is now added to local JSON file.")
            create_logs("add_collection", "local_json",
                        f"Collection '{collection_name}' is now added to local JSON file.",
                        status='info')

        if len(data) < 1:
            current_app.logger.error("No data provided for Firestore add.")
            return False

        if type(data) != dict and add_type == "new document":
            current_app.logger.error("Invalid data type for Firestore add into document.")
            return False

        if add_type == "new collection":
            db.collection(collection_name).document(doc_id).set(data)
            create_logs("add_collection", "firebase_db", f"Collection '{collection_name}' is now added.", status='info')
            return True

        doc_ref = db.collection(collection_name).document(doc_id)

        if not doc_ref.get().exists:
            current_app.logger.error(f"Document '{doc_id}' does not exist in collection '{collection_name}'.")
            return False

        if add_type == "exist field":
            doc_ref.update({field_name: data})
            create_logs("add_exist_field", "firebase_db",
                        f"Field '{field_name}' in document '{doc_id}' is now updated.", )
            return True

        elif add_type == "new document":
            db.collection(collection_name).add(data)
            create_logs("new_document", "firebase_db", f"Document '{doc_id}' is now added.", status='info')
            return True

        elif add_type == "new field":
            doc_ref = db.collection(collection_name).document(doc_id)
            doc_ref.set({field_name: data})
            create_logs("new_field", "firebase_db", f"Field '{field_name}' in document '{doc_id}' is now added.", )
            return True

        else:
            current_app.logger.error("Invalid firebase add type. Please use 'field', 'new document', or 'new field'.")
            return False

    except Exception as e:
        current_app.logger.error(f"Failed to add data to Firestore: {e}")
        create_logs("add_data", "firebase_db", f"Failed to add data to Firestore: {e}", status='error')
        return False


def update_data(collection_name, doc_id, update_type="one", data={}, field_name="") -> bool:
    global db

    """Update a document in the Firestore database."""
    try:
        if len(data) < 1:
            current_app.logger.error("No data provided for Firestore update.")
            return False

        doc_ref = db.collection(collection_name)

        if not doc_ref.limit(1).get():
            current_app.logger.error(f"Collection '{collection_name}' does not exist in Firestore.")
            return False

        doc_ref = doc_ref.document(doc_id)

        if not doc_ref.get().exists:
            current_app.logger.error(f"Document '{doc_id}' does not exist in collection '{collection_name}'.")
            return False

        if update_type == "one":
            doc_ref.update(data)
            create_logs("update_one", "firebase_db", f"Document '{doc_id}' is now updated.", status='info')
            return True
        elif update_type == "field":
            doc = doc_ref.get()
            current_data = doc.to_dict()
            current_data[field_name] = data
            doc_ref.update(current_data)
            create_logs("update_field", "firebase_db", f"Field '{field_name}' in document '{doc_id}' is now updated.", )
            return True
        elif update_type == "all":
            data = str2json(data)
            doc_ref.update(data)
            create_logs("update_all", "firebase_db", f"Document '{doc_id}' is now updated.", status='info')
            return True
        else:
            current_app.logger.error("Invalid firebase update type. Please use 'one', 'field', or 'all'.")
            return False

    except Exception as e:
        current_app.logger.error(f"Failed to update data in Firestore: {e}")
        create_logs("firebase_db", "firebase_db", f"Failed to update data in Firestore: {e}", status='error')
        return False


def delete_data(collection_name, doc_id, delete_type="document", field_name="") -> bool:
    global db
    """Delete a document from the Firestore database."""
    try:
        if doc_id == "":
            current_app.logger.error("No document ID provided for Firestore delete.")
            return False

        if field_name == "" and (delete_type == "del_field" or delete_type == "empty_field"):
            current_app.logger.error("No field name provided for Firestore delete.")
            return False

        doc_ref = db.collection(collection_name)

        if not doc_ref.limit(1).get():
            current_app.logger.error(f"Collection '{collection_name}' does not exist in Firestore.")
            return False

        doc_ref = doc_ref.document(doc_id)

        if not doc_ref.get().exists:
            current_app.logger.error(
                f"Cant Delete, Document '{doc_id}' does not exist in collection '{collection_name}'.")
            return False

        if delete_type == "document":
            doc_ref.delete()
            current_app.logger.info(f"Document '{doc_id}' is now deleted.")
            create_logs("delete_document", "firebase_db", f"Document '{doc_id}' is now deleted.", status='warning')
            return True
        elif delete_type == "del_field":
            doc = doc_ref.get()
            current_data = doc.to_dict()
            del current_data[field_name]
            doc_ref.update(current_data)
            current_app.logger.info(f"Field '{field_name}' in document '{doc_id}' is now deleted.")
            create_logs("delete_field", "firebase_db", f"Field '{field_name}' in document '{doc_id}' is now deleted.",
                        status='warning')
            return True
        elif delete_type == "empty_field":
            doc_ref.update({field_name: ""})
            current_app.logger.info(f"Field '{field_name}' in document '{doc_id}' is now empty.")
            create_logs("empty_field", "firebase_db", f"Field '{field_name}' in document '{doc_id}' is now empty.",
                        status='warning')
            return True
        elif delete_type == "collection":
            docs = doc_ref.stream()
            for doc in docs:
                doc.reference.delete()
            create_logs("delete_collection", "firebase_db", f"Collection '{collection_name}' is now deleted.",
                        status='warning')
            return True
        else:
            current_app.logger.error(
                "Invalid firebase delete type. Please use 'document', 'del_field', or 'empty_field'.")
            return False

    except Exception as e:
        current_app.logger.error(f"Failed to delete data from Firestore: {e}")
        create_logs("delete_data", "firebase_db", f"Failed to delete data from Firestore: {e}", status='error')
        return False


def get_collection(collection_name) -> any:
    global db
    """Retrieve all documents from a collection in the Firestore database."""
    try:
        doc_ref = db.collection(collection_name)

        if not doc_ref.limit(1).get():
            current_app.logger.error(f"Collection '{collection_name}' does not exist in Firestore.")
            return ""

        docs = doc_ref.get()
        create_logs("get_collection", "firebase_db", f"Retrieved all transactions from collection '{collection_name}'.",
                    status='info')
        return docs

    except Exception as e:
        current_app.logger.error(f"Failed to retrieve data from Firestore: {e}")
        create_logs("get_collection", "firebase_db", f"Failed to retrieve data from Firestore: {e}", status='error')
        return ""


def get_data(collection_name, doc_id="", gettype="field", field_name="") -> any:
    global db
    """Retrieve a specific field from a document in the Firestore database."""
    try:
        doc_ref = db.collection(collection_name)

        if not doc_ref.limit(1).get():
            current_app.logger.error(f"Cant get data, Collection '{collection_name}' does not exist in Firestore.")
            return ""

        elif gettype == "collection":
            docs = doc_ref.stream()
            docs = {doc.id: doc.to_dict() for doc in docs}

            create_logs("get_collection", "firebase_db",
                        f"Retrieved all transactions from collection '{collection_name}'.",
                        status='info')
            return docs

        doc = doc_ref.document(doc_id).get()
        if not doc.exists:
            current_app.logger.error(
                f"Cant get data, Document '{doc_id}' does not exist in collection '{collection_name}'.")
            return ""

        data = doc.to_dict()
        if field_name not in data:
            current_app.logger.error(f"Cant get data, Field '{field_name}' does not exist in document '{doc_id}'.")
            return ""

        if gettype == "document":
            create_logs("get_document", "firebase_db",
                        f"Retrieved document '{doc_id}' from collection '{collection_name}'.", status='info')
            return data

        elif gettype == "field" or field_name != "":
            create_logs("get_field", "firebase_db", f"Retrieved field '{field_name}' from document '{doc_id}'.",
                        status='info')
            return data[field_name]

        else:
            current_app.logger.error("Invalid firebase get type. Please use 'field', 'document', or 'collection'.")
            return ""

    except Exception as e:
        create_logs("get_data", "firebase_db", f"Failed to retrieve data from Firestore: {e}", status='error')
        return ""


# dict.string to json
def str2json(data) -> dict:
    try:
        return json.loads(data)
    except Exception as e:
        current_app.logger.error(f"Failed to convert string to JSON: {e}")
        return {}


def fb_str2json(collection_name, doc_id, field_name) -> dict:
    try:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc = doc_ref.get()
        data = doc.to_dict()
        return str2json(data[field_name])
    except Exception as e:
        current_app.logger.error(f"Failed to convert string to JSON: {e}")
        return {}


def fb_json2str(collection_name, doc_id, field_name, data) -> bool:
    try:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc_ref.update({field_name: json.dumps(data)})
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to convert JSON to string: {e}")
        return False


# firestore to local json function

def fb2local() -> bool:
    filepath = "database/local_db.json"
    check_data = {}

    try:
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=4, ensure_ascii=False)
            current_app.logger.info("Local JSON file created.")
            create_logs("create_file", "local_json", "Local JSON file created.", status='info')
        else:
            with open(filepath, 'r', encoding='utf-8') as f:
                check_data = json.load(f)

        if "_local" not in check_data:
            check_data["_local"] = dict({})

        if "collections" not in check_data:
            check_data["_local"]["collections"] = []

        if "local_check" not in check_data:
            check_data["_local"]["check"] = {
                "last_update": "",
                "last_check": "",
                "latest": True,
                "updated_collections": [],
                "history": [],
            }

        collections = get_collection_names()
        for collection in collections:
            if collection != "CONFIG":
                if collection not in check_data["_local"]["collections"]:
                    check_data["_local"]["collections"].append(collection)
                data = get_data(collection, gettype="collection")
                check_data[collection] = data
                current_app.logger.info(f"Data from collection '{collection}' saved to local JSON file.")
                create_logs(f"catch-{collection}", "local_json",
                            f"Data from collection '{collection}' saved to local JSON file.", status='info')

        check_data["_local"]["check"]["last_update"] = datetime_now()
        check_data["_local"]["check"]["latest"] = True
        check_data["_local"]["check"]["last_check"] = datetime_now()

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(check_data, f, indent=4, ensure_ascii=False)

        return True

    except Exception as e:
        current_app.logger.error(f"Failed to save data to local JSON: {e}")
        create_logs("local_json", "local_json", f"Failed to save data to local JSON: {e}", status='error')
        return False


# local saving function
def local2fb(collection_name: list, doc_id, field_name, data):
    '''Save local data to Firebase'''
    pass


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



