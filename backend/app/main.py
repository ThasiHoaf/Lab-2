from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Giữ nguyên phần Auth
from backend.app.routers.auth_routers import router as auth_router
from backend.app.routers.analyze_routers import router as analyze_router

app = FastAPI(
    title="Age & Gender Recognition API",
    description="Hệ thống API phân tích độ tuổi và giới tính thông qua hình ảnh sử dụng Deep Learning.",
    version="1.0.0"
)

# Cấu hình CORS để Frontend có thể giao tiếp với Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501", # URL mặc định của Streamlit Frontend
        "http://127.0.0.1:8501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gắn các Routers vào ứng dụng
app.include_router(auth_router)
app.include_router(analyze_router)

@app.get("/", tags=["system"])
def read_root():
    """
    Trang chủ của hệ thống API.
    """
    return {
        "message": "Chào mừng đến với hệ thống API Phân tích Khuôn mặt (Age & Gender Recognition)",
        "docs_url": "/docs",
        "health_check": "/health"
    }

@app.get("/health", tags=["system"])
def health():
    """
    API kiểm tra tình trạng "sức khỏe" của server.
    Thường được sử dụng bởi các hệ thống Load Balancer để xem server có đang hoạt động hay không.
    """
    return {"status": "ok", "service": "Age & Gender API is running"}