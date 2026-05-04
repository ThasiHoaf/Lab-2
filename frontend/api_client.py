import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000/api/v1"

# Tự động lấy Firebase Web API Key từ file .streamlit/secrets.toml
FIREBASE_WEB_API_KEY = "AIzaSyDHwgl33gENvd7_IiNJmGCGHU-4wlL3UYI"

def signup(email, password):
    """Đăng ký tài khoản trực tiếp qua Firebase REST API"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
         error_msg = response.json().get("error", {}).get("message", "Lỗi không xác định")
         raise requests.HTTPError(error_msg)
         
    return response.json()

def login(email, password):
    """Đăng nhập trực tiếp qua Firebase REST API để lấy Token xịn"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    
    if response.status_code != 200:
         error_msg = response.json().get("error", {}).get("message", "Sai tài khoản hoặc mật khẩu")
         raise requests.HTTPError(error_msg)
         
    data = response.json()
    # Trả về đúng format mà app.py đang mong đợi
    return {
        "email": data["email"], 
        "idToken": data["idToken"], 
        "uid": data["localId"]
    }

# Các hàm khác như google_login, analyze_image, get_analysis_history giữ nguyên...
def google_login(id_token):
    # API giả lập xử lý sau khi lấy được token từ Google
    return {"email": "google_user@gmail.com", "idToken": id_token}

def analyze_image(file_bytes, filename, content_type, id_token):
    url = f"{API_BASE_URL}/analyze/"
    files = {"file": (filename, file_bytes, content_type)}
    headers = {"Authorization": f"Bearer {id_token}"} if id_token else {}
    response = requests.post(url, files=files, headers=headers, timeout=600)
    response.raise_for_status()
    return response.json()

def get_analysis_history(id_token):
    url = f"{API_BASE_URL}/analyze/history"
    headers = {"Authorization": f"Bearer {id_token}"} if id_token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()