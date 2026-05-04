from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

class AuthRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(request: AuthRequest):
    # Endpoint giả lập xử lý xác thực
    # TODO: Tích hợp logic xử lý Database hoặc Firebase tại đây
    return {"email": request.email, "idToken": "fake-jwt-token"}

@router.post("/signup")
def signup(request: AuthRequest):
    # Endpoint giả lập đăng ký tài khoản
    return {"message": "Đăng ký thành công", "email": request.email}