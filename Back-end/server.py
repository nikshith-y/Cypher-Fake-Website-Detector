import hashlib
import requests
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore
cred = credentials.Certificate("firebase-key.json")  # Your Firebase credentials
firebase_admin.initialize_app(cred)
db = firestore.client()

# Google Safe Browsing API Key (Replace with your key)
GOOGLE_API_KEY = "AIzaSyARrKHqsTac_wm-xvHp4nkG2yKlB_eHhBc"
SAFE_BROWSING_URL = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key=AIzaSyARrKHqsTac_wm-xvHp4nkG2yKlB_eHhBc"

app = Flask(__name__)

def check_google_safe_browsing(url):
    """Check URL using Google Safe Browsing API"""
    payload = {
        "client": {"clientId": "cypher-fwd", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": url}]
        }
    }
    
    response = requests.post(SAFE_BROWSING_URL, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        if "matches" in data:
            return "unsafe"  # URL is unsafe
    return "safe"  # URL is safe

@app.route("/detect", methods=["POST"])
def detect():
    data = request.json
    url = data.get("url")  # Get the URL from the request

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Hash the URL for Firestore document ID
    hashed_url = hashlib.md5(url.encode()).hexdigest()

    # Check Firestore first
    doc_ref = db.collection("scanned_urls").document(hashed_url)
    doc = doc_ref.get()

    if doc.exists:
        return jsonify({"status": "URL found", "data": doc.to_dict()})

    # If not found, check Google Safe Browsing
    verdict = check_google_safe_browsing(url)

    # Store result in Firestore
    doc_ref.set({"url": url, "verdict": verdict})

    return jsonify({"status": "URL scanned", "verdict": verdict})

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def home():
    return "Cypher - Fake Website Detector API is running!"