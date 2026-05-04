import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

from .config import settings

def get_firebase_auth():
    """Khởi tạo và trả về dịch vụ xác thực của Firebase Admin."""
    init_firebase_admin()
    return auth

def init_firebase_admin():
    """Khởi tạo Firebase Admin SDK nếu chưa được khởi tạo."""
    if not firebase_admin._apps:
        cred_dict = settings.get_firebase_admin_creds()
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

def get_firestore():
    """Trả về một đối tượng client của Firestore."""
    init_firebase_admin()
    return firestore.client()