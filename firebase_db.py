import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('creds/firebase_cred.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def add_transaction(transaction_data):
    """Add a new transaction to the Firestore database."""
    transaction_ref = db.collection('transactions').document()
    transaction_ref.set(transaction_data)


def get_transactions():
    """Retrieve all transactions from the Firestore database."""
    transactions = db.collection('transactions').stream()
    return [doc.to_dict() for doc in transactions]
