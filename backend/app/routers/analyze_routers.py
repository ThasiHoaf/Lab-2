from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Header
from fastapi.concurrency import run_in_threadpool
from datetime import datetime

# Import từ service Firebase ✅ UNCOMMENTED
from backend.app.services.firestore_service import save_analysis_record, load_analysis_history
# Import các service và schema đã được định nghĩa
from backend.app.services.ml_service import predict_age_gender
from backend.app.schemas.analyze_schemas import AnalyzeResponse
from backend.app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/api/v1/analyze",
    tags=["Analyze AI"]
)

@router.post("/", response_model=AnalyzeResponse)
async def analyze_image(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)  # ✅ Thêm xác thực người dùng
):
    """
    API nhận hình ảnh từ Frontend, phân tích độ tuổi, giới tính và lưu vào Firestore.
    """
    # 1. Kiểm tra định dạng file
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Vui lòng tải lên một tệp hình ảnh hợp lệ (jpg, png,...)")
    
    try:
        # 2. Đọc byte của ảnh từ bộ nhớ
        image_bytes = await file.read()
        
        # 3. Chuyển cho mô hình AI xử lý (đã có trong ml_service.py)
        # Chạy ngầm trong ThreadPool để không làm đơ Server (An toàn vì đã dùng Lock)
        prediction = await run_in_threadpool(predict_age_gender, image_bytes)
        
        # 4. Lưu dữ liệu vào Firestore ✅ UNCOMMENTED & FIXED
        save_to_database(
            uid=current_user["uid"],  # ✅ Sử dụng UID từ người dùng đã xác thực
            age=prediction["age"],
            gender=prediction["gender"],
            confidence=prediction["confidence"],
            timestamp=datetime.now()
        )
        
        # 5. Trả kết quả về cho Frontend theo chuẩn AnalyzeResponse
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống trong quá trình phân tích: {str(e)}")
        
@router.get("/history")
def get_history(current_user = Depends(get_current_user)):  # ✅ Thêm xác thực
    """
    API lấy danh sách lịch sử phân tích của người dùng.
    """
    try:
        # ✅ Gọi Firestore thực tế thay vì mock data
        return load_analysis_history(uid=current_user["uid"], limit=10)
    except Exception as e:
        print(f"[Error] Lỗi lấy lịch sử: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def save_to_database(uid: str, age, gender, confidence, timestamp):
    """
    Lưu dữ liệu vào Firestore ✅ FIXED
    """
    try:
        # ✅ Uncommented - Thực sự gọi hàm lưu Firestore
        save_analysis_record(uid, age, gender, confidence)
        print(f"[Database] ✅ Đã lưu bản ghi: {gender}, {age} tuổi với độ tin cậy {confidence*100:.1f}% cho user {uid}")
    except Exception as e:
        print(f"[Database] ❌ Lỗi khi lưu: {str(e)}")