import firebase_admin
from firebase_admin import credentials, firestore

# Path to your service account JSON file
cred = credentials.Certificate("./cypher-fwd-firebase-adminsdk-fbsvc-1b55ffac71.json")

# Initialize Firebase Admin
firebase_admin.initialize_app(cred)

# Get Firestore database reference
db = firestore.client()

print("🔥 Firebase connected successfully!")