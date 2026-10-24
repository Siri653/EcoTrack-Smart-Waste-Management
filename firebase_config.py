
import os
import firebase_admin
from firebase_admin import credentials, auth, db

DATABASE_URL = "https://smart-waste-management-7d746-default-rtdb.asia-southeast1.firebasedatabase.app"

if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        "databaseURL":"https://smart-waste-management-7d746-default-rtdb.asia-southeast1.firebasedatabase.app"
    })

def verify_firebase_token(id_token):
    """Verify a Firebase ID token and return the decoded user claims."""
    return auth.verify_id_token(id_token)
