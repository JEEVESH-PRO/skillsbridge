import os
import firebase_admin
from firebase_admin import credentials, firestore, auth

_firebase_app = None
_db_firestore = None

def init_firebase(cred_path=None):
    """
    Initializes Firebase Admin SDK using a service account JSON file.
    If cred_path is not specified, looks for 'firebase_service_account.json' in the project directory.
    """
    global _firebase_app, _db_firestore

    if _firebase_app:
        return _db_firestore

    if not cred_path:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cred_path = os.environ.get('FIREBASE_CREDENTIALS_PATH') or os.path.join(base_dir, 'firebase_service_account.json')

    if os.path.exists(cred_path):
        try:
            cred = credentials.Certificate(cred_path)
            _firebase_app = firebase_admin.initialize_app(cred)
            _db_firestore = firestore.client()
            print(f"[Firebase] Successfully connected to Firebase Admin SDK using {cred_path}")
            return _db_firestore
        except Exception as e:
            print(f"[Firebase Warning] Failed to initialize Firebase with credentials: {e}")
    else:
        print(f"[Firebase Info] Service account key file not found at '{cred_path}'. Add your 'firebase_service_account.json' to enable Firestore cloud database sync.")
    
    return None

def get_firestore_db():
    return _db_firestore or init_firebase()

def sync_user_to_firestore(user_dict):
    """
    Syncs a user record to Cloud Firestore collection 'users'
    """
    db = get_firestore_db()
    if not db:
        return False
    try:
        user_id = str(user_dict.get('id') or user_dict.get('email'))
        db.collection('users').document(user_id).set(user_dict, merge=True)
        return True
    except Exception as e:
        print(f"[Firebase Error] Syncing user to Firestore: {e}")
        return False

def sync_job_to_firestore(job_dict):
    """
    Syncs a job posting to Cloud Firestore collection 'jobs'
    """
    db = get_firestore_db()
    if not db:
        return False
    try:
        job_id = str(job_dict.get('id'))
        db.collection('jobs').document(job_id).set(job_dict, merge=True)
        return True
    except Exception as e:
        print(f"[Firebase Error] Syncing job to Firestore: {e}")
        return False
