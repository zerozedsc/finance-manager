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


def add_collection(collection_name, data=""):
    global db
    """Add a new collection to the Firestore database."""
    try:
        if type(data) != dict:
            current_app.logger.error("Invalid data type for Firestore add.")
            return False

        db.collection(collection_name).add(data)
        create_logs("firebase_db", "firebase_db", f"Collection '{collection_name}' is now added.", status='info')
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to add collection to Firestore: {e}")
        create_logs("firebase_db", "firebase_db", f"Failed to add collection to Firestore: {e}", status='error')
        return False


def add_data(collection_name, add_type="field", doc_id="", field_name="", data=""):
    global db

    """Add a new document to the Firestore database."""
    try:
        if len(data) < 1:
            current_app.logger.error("No data provided for Firestore add.")
            return False

        if type(data) != dict and add_type == "new document":
            current_app.logger.error("Invalid data type for Firestore add into document.")
            return False

        if add_type == "exist field":
            doc_ref = db.collection(collection_name).document(doc_id)
            doc_ref.update({field_name: data})
            create_logs("firebase_db", "firebase_db", f"Field '{field_name}' in document '{doc_id}' is now updated.", )
            return True
        elif add_type == "new document":
            db.collection(collection_name).add(data)
            create_logs("firebase_db", "firebase_db", f"Document '{doc_id}' is now added.", status='info')
            return True
        elif add_type == "new field":
            doc_ref = db.collection(collection_name).document(doc_id)
            doc_ref.set({field_name: data})
            create_logs("firebase_db", "firebase_db", f"Field '{field_name}' in document '{doc_id}' is now added.", )
            return True
        else:
            current_app.logger.error("Invalid firebase add type. Please use 'field', 'new document', or 'new field'.")
            return False

    except Exception as e:
        current_app.logger.error(f"Failed to add data to Firestore: {e}")
        create_logs("firebase_db", "firebase_db", f"Failed to add data to Firestore: {e}", status='error')
        return False


def update_data(collection_name, update_type="one", data="", doc_id="", field_name="") -> bool:
    global db

    """Update a document in the Firestore database."""
    try:
        if len(data) < 1:
            current_app.logger.error("No data provided for Firestore update.")
            return False

        if update_type == "one":
            db.collection(collection_name).document(doc_id).update(data)
            create_logs("firebase_db", "firebase_db", f"Document '{doc_id}' is now updated.", status='info')
            return True
        elif update_type == "field":
            doc_ref = db.collection(collection_name).document(doc_id)
            doc = doc_ref.get()
            current_data = doc.to_dict()
            current_data[field_name] = data
            doc_ref.update(current_data)
            create_logs("firebase_db", "firebase_db", f"Field '{field_name}' in document '{doc_id}' is now updated.", )
            return True
        elif update_type == "all":
            doc_ref = db.collection(collection_name).document(doc_id)
            data = string_to_json(data)
            doc_ref.update(data)
            create_logs("firebase_db", "firebase_db", f"Document '{doc_id}' is now updated.", status='info')
            return True
        else:
            current_app.logger.error("Invalid firebase update type. Please use 'one', 'field', or 'all'.")
            return False

    except Exception as e:
        current_app.logger.error(f"Failed to update data in Firestore: {e}")
        create_logs("firebase_db", "firebase_db", f"Failed to update data in Firestore: {e}", status='error')
        return False


def get_collection(collection_name) -> dict:
    global db
    """Retrieve all transactions from the Firestore database."""
    try:
        transactions = db.collection(collection_name).stream()
        # Create a dictionary where each key is the document name (ID) and its value is the document data
        transactions_dict = {doc.id: doc.to_dict() for doc in transactions}

        current_app.logger.info(f"Retrieved all transactions from collection '{collection_name}'.")
        create_logs("firebase_db", "firebase_db", f"Retrieved all transactions from collection '{collection_name}'.",
                    status='info')

    except Exception as e:
        current_app.logger.error(f"Failed to retrieve transactions from Firestore: {e}")
        create_logs("firebase_db", "firebase_db", f"Failed to retrieve transactions from Firestore: {e}", status='error')
        transactions_dict = {}

    return transactions_dict


def delete_collection(collection_name):
    global db
    """Delete a collection from the Firestore database."""
    try:
        collection_ref = db.collection(collection_name)
        docs = collection_ref.stream()
        for doc in docs:
            doc.reference.delete()
        current_app.logger.info(f"Collection '{collection_name}' is now deleted.")
        create_logs("firebase_db", "firebase_db", f"Collection '{collection_name}' is now deleted.", status='warning')
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to delete collection from Firestore: {e}")
        create_logs("firebase_db", "firebase_db", f"Failed to delete collection from Firestore: {e}", status='error')
        return False


def delete_data(collection_name, delete_type="document", doc_id="", field_name="") -> bool:
    global db
    """Delete a document from the Firestore database."""
    try:
        if doc_id == "":
            current_app.logger.error("No document ID provided for Firestore delete.")
            return False

        if field_name == "" and (delete_type == "del_field" or delete_type == "empty_field"):
            current_app.logger.error("No field name provided for Firestore delete.")
            return False

        if delete_type == "document":
            db.collection(collection_name).document(doc_id).delete()
            current_app.logger.info(f"Document '{doc_id}' is now deleted.")
            create_logs("firebase_db", "firebase_db", f"Document '{doc_id}' is now deleted.", status='warning')
            return True
        elif delete_type == "del_field":
            doc_ref = db.collection(collection_name).document(doc_id)
            doc = doc_ref.get()
            current_data = doc.to_dict()
            del current_data[field_name]
            doc_ref.update(current_data)
            current_app.logger.info(f"Field '{field_name}' in document '{doc_id}' is now deleted.")
            create_logs("firebase_db", "firebase_db", f"Field '{field_name}' in document '{doc_id}' is now deleted.",
                        status='warning')
            return True
        elif delete_type == "empty_field":
            doc_ref = db.collection(collection_name).document(doc_id)
            doc_ref.update({field_name: ""})
            current_app.logger.info(f"Field '{field_name}' in document '{doc_id}' is now empty.")
            create_logs("firebase_db", "firebase_db", f"Field '{field_name}' in document '{doc_id}' is now empty.",
                        status='warning')
            return True
        else:
            current_app.logger.error("Invalid firebase delete type. Please use 'document' or 'field'.")
            return False

    except Exception as e:
        current_app.logger.error(f"Failed to delete data from Firestore: {e}")
        create_logs("firebase_db", "firebase_db", f"Failed to delete data from Firestore: {e}", status='error')
        return False


# dict.string to json
def string_to_json(data) -> dict:
    try:
        return json.loads(data)
    except Exception as e:
        current_app.logger.error(f"Failed to convert string to JSON: {e}")
        return {}


def firebase_str2json(collection_name, doc_id, field_name) -> dict:
    try:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc = doc_ref.get()
        data = doc.to_dict()
        return string_to_json(data[field_name])
    except Exception as e:
        current_app.logger.error(f"Failed to convert string to JSON: {e}")
        return {}


def firebase_json2str(collection_name, doc_id, field_name, data) -> bool:
    try:
        doc_ref = db.collection(collection_name).document(doc_id)
        doc_ref.update({field_name: json.dumps(data)})
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to convert JSON to string: {e}")
        return False


# firestore to local json function

def firebase_to_local() -> bool:
    filepath = "database/local_db.json"
    check_data = {}

    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4, ensure_ascii=False)
        current_app.logger.info("Local JSON file created.")
        create_logs("local_json", "local_json", "Local JSON file created.", status='info')
    else:
        with open(filepath, 'r', encoding='utf-8') as f:
            check_data = json.load(f)

    try:
        if "_local" not in check_data:
            check_data["_local"] = dict({})

        if "collections" not in check_data:
            check_data["_local"]["collections"] = []

        if "local_check" not in check_data:
            check_data["_local"]["check"] = {
                "last_update": "",
                "last_check": "",
                "latest": True,
                "updated_collection": [],
                "history": [],
            }

        collections = get_collection_names()
        for collection in collections:
            if collection not in check_data["_local"]["collections"]:
                check_data["_local"]["collections"].append(collection)
            data = get_collection(collection)
            check_data[collection] = data
            current_app.logger.info(f"Data from collection '{collection}' saved to local JSON file.")
            create_logs("local_json", "local_json",
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
