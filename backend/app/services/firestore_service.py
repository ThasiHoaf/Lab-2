from datetime import datetime, timezone
from backend.app.core.firebase_config import get_firestore
from firebase_admin import firestore

db = get_firestore()

def save_analysis_record(uid: str, age: int, gender: str, confidence: float):
    """
    Lưu kết quả nhận diện vào Firestore.
    Cấu trúc phân cấp chuẩn: users/{uid}/history/{document_id}
    Việc lưu trữ riêng biệt theo uid giúp đảm bảo bảo mật dữ liệu cá nhân.
    """
    doc = {
        "age": age,
        "gender": gender,
        "confidence": confidence,
        "ts": datetime.now(timezone.utc)
    }
    # Sử dụng collection 'users' thay vì 'chats'
    db.collection("users").document(uid).collection("history").add(doc)

def load_analysis_history(uid: str, limit: int = 10):
    """
    Truy xuất lịch sử nhận diện của người dùng, sắp xếp từ mới nhất đến cũ nhất.
    """
    q = (
        db.collection("users")
        .document(uid)
        .collection("history")
        .order_by("ts", direction=firestore.Query.DESCENDING)
        .limit(limit)
    )

    docs = list(q.stream())
    
    results = []
    for d in docs:
        data = d.to_dict()
        results.append({
            "age": data.get("age", 0),
            "gender": data.get("gender", "Unknown"),
            "confidence": data.get("confidence", 0.0),
            "timestamp": data.get("ts").isoformat() if data.get("ts") else ""
        })
        
    return results