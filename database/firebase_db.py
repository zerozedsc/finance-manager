import firebase_admin
from firebase_admin import credentials, firestore
from flask import current_app

# Initialize Firebase Admin SDK
cred = credentials.Certificate('creds/firebase_cred.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_firestore_data(collection_name):
    global db
    try:
        collection_ref = db.collection(collection_name)
        docs = collection_ref.stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        current_app.logger.error(f"Failed to fetch data from Firestore: {e}")
        return []


def get_collection_names():
    global db
    """Retrieve all collection names from the Firestore database."""
    collections = db.collections()
    return [collection.id for collection in collections]


def add_data(collection_name, data):
    global db
    """Add a new transaction to the Firestore database."""
    transaction_ref = db.collection(collection_name).document()
    transaction_ref.set(data)


def get_collection(collection_name):
    global db
    """Retrieve all transactions from the Firestore database."""
    transactions = db.collection(collection_name).stream()
    return [doc.to_dict() for doc in transactions]


def delete_collection(collection_name):
    global db
    """Delete a collection from the Firestore database."""
    try:
        collection_ref = db.collection(collection_name)
        docs = collection_ref.stream()
        for doc in docs:
            doc.reference.delete()
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to delete collection from Firestore: {e}")
        return False


def delete_data(collection_name, doc_id):
    global db
    """Delete a document from the Firestore database."""
    try:
        db.collection(collection_name).document(doc_id).delete()
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to delete data from Firestore: {e}")
        return False


def update_data(collection_name, doc_id, data):
    global db
    """Update a document in the Firestore database."""
    try:
        db.collection(collection_name).document(doc_id).update(data)
        return True
    except Exception as e:
        current_app.logger.error(f"Failed to update data in Firestore: {e}")
        return False

