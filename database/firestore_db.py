import os
import json
import tempfile
import firebase_admin
from firebase_admin import credentials, firestore

_firestore_client = None
_firestore_app = None


def _load_credentials():
    """Return a firebase_admin credentials object, preferring env vars.

    Resolution order:
      1. FIREBASE_SERVICE_ACCOUNT_JSON (raw JSON string passed via env var)
      2. FIREBASE_SERVICE_ACCOUNT (base64-encoded JSON)
      3. GOOGLE_APPLICATION_CREDENTIALS (path to JSON file)
      4. Local firebase_service_account.json next to this file
      5. Application Default Credentials (default -> None)
    """
    raw = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
    if raw:
        return credentials.Certificate(json.loads(raw))

    b64 = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
    if b64:
        import base64
        payload = base64.b64decode(b64)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as fh:
            fh.write(payload.decode('utf-8'))
            temp_path = fh.name
        return credentials.Certificate(temp_path)

    cred_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'firebase_service_account.json'
    )

    if os.path.exists(cred_path):
        return credentials.Certificate(cred_path)

    return None


def _initialize_app(cred):
    if not firebase_admin._apps:
        if cred is not None:
            return firebase_admin.initialize_app(cred)
        return firebase_admin.initialize_app()
    # Reuse whichever app already exists
    return list(firebase_admin._apps.values())[0]


def init_firestore():
    global _firestore_client, _firestore_app
    if _firestore_client:
        return _firestore_client

    cred = _load_credentials()
    _firestore_app = _initialize_app(cred)
    _firestore_client = firestore.client(_firestore_app)
    return _firestore_client


def get_db():
    global _firestore_client
    if not _firestore_client:
        init_firestore()
    return _firestore_client