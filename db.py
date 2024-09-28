import firebase_admin
from firebase_admin import firestore, credentials

# Application Default credentials are automatically created.
creds = credentials.Certificate("firebase_creds.json")
app = firebase_admin.initialize_app(creds)
db = firestore.client()
