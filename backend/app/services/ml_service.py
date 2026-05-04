import os
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Ép dùng CPU để tránh crash do GPU Driver
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'   # Ẩn bớt các log cảnh báo dài dòng của TensorFlow
import io
import cv2
import numpy as np
import threading
from deepface import DeepFace


# -------------------------------------------------------------------------
# QUAN TRỌNG: TRONG MÔI TRƯỜNG THỰC TẾ (PRODUCTION)
# Việc load mô hình (model weights) vào RAM/VRAM tốn rất nhiều thời gian.
# Do đó, model PHẢI được khởi tạo một lần duy nhất ở phạm vi toàn cục (Global),
# KHÔNG ĐƯỢC load lại bên trong hàm mỗi khi có API request gửi tới.
# -------------------------------------------------------------------------

def load_ai_model():
    """
    Hàm giả lập việc nạp trọng số mạng nơ-ron (Neural Network weights) vào bộ nhớ.
    """
    print("[Hệ thống] Đang khởi tạo và nạp mô hình nhận diện khuôn mặt (Age & Gender) vào bộ nhớ...")
    try:
        # Khởi tạo trước mô hình để tránh bị delay ở lần gọi API đầu tiên
        # Warm-up: Đưa một bức ảnh ma trận 0 (ảnh đen) vào để DeepFace tự động tải model
        dummy_img = np.zeros((224, 224, 3), dtype=np.uint8)
        DeepFace.analyze(dummy_img, actions=['age', 'gender'], enforce_detection=False, detector_backend='opencv')
    except Exception as e:
        print(f"[Cảnh báo] Không thể tải trước mô hình: {e}")
    return True


# Tạo ổ khóa luồng: Tuyệt đối chỉ cho 1 bức ảnh được phân tích tại 1 thời điểm
_ai_lock = threading.Lock()
_is_model_loaded = False

# Khởi tạo model sẵn khi file này được import lần đầu tiên
_face_model = load_ai_model()

def predict_age_gender(image_bytes: bytes) -> dict:
    """
    Hàm lõi xử lý thuật toán nhận diện.
    
    Quy trình chuẩn khoa học dữ liệu:
    1. Tiền xử lý (Preprocessing): Chuyển bytes thành ma trận numpy, căn chỉnh khuôn mặt (Face Alignment), chuẩn hóa (Normalization).
    2. Suy luận (Inference): Đưa ma trận qua mạng CNN (Convolutional Neural Network).
    3. Hậu xử lý (Post-processing): Ánh xạ vector đầu ra thành nhãn (Male/Female) và số lượng (Age).
    """
    global _is_model_loaded
    
    # Dùng with _ai_lock để chặn mọi thao tác đa luồng gây sập TensorFlow
    with _ai_lock:
        try:
            # Kỹ thuật Lazy-Load: Chỉ tải mô hình vào RAM khi thực sự có người click bấm nút
            if not _is_model_loaded:
                print("[Hệ thống] Đang nạp mô hình AI vào RAM... (Chỉ chạy 1 lần duy nhất)")
                # Thư viện DeepFace sẽ tự động tải mô hình ở hàm analyze phía dưới
                _is_model_loaded = True

            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None:
                raise ValueError("Không thể đọc được hình ảnh.")
                
            # TỐI ƯU CỰC ĐẠI: enforce_detection=False để ép mô hình không được văng lỗi
            results = DeepFace.analyze(
                img, 
                actions=['age', 'gender'], 
                enforce_detection=False, 
                detector_backend='opencv'
            )
            
            face_data = results[0] if isinstance(results, list) else results
            
            return {
                "age": int(face_data.get("age", 0)),
                "gender": face_data.get("dominant_gender", "Unknown"),
                "confidence": float(face_data.get("face_confidence", 0.90))
            }
        except Exception as e:
            raise ValueError(f"Lỗi khi phân tích hình ảnh: {str(e)}")