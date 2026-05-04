# AI Nhận Diện Khuôn Mặt

Ứng dụng này gồm hai phần chính:

- **Backend**: FastAPI cung cấp API đăng ký, đăng nhập và phân tích ảnh.
- **Frontend**: Streamlit cho giao diện người dùng đăng nhập/đăng ký và tải ảnh để phân tích.

## 🚀 Tính năng chính

- Đăng ký / đăng nhập người dùng
- Đăng nhập với Google (cần cấu hình trong secrets)
- Tải ảnh lên và phân tích độ tuổi + giới tính
- Lưu lịch sử phân tích
- Backend/Frontend tách riêng, dễ mở rộng

## 📁 Cấu trúc thư mục

- `backend/app/main.py` – khởi tạo FastAPI và đăng ký router
- `backend/app/routers/auth_routers.py` – xử lý đăng ký/đăng nhập
- `backend/app/routers/analyze_routers.py` – xử lý phân tích ảnh
- `frontend/app.py` – giao diện Streamlit
- `frontend/api_client.py` – gọi API backend từ frontend
- `requirements.txt` – các thư viện Python cần cài

## 📦 Yêu cầu

- Python 3.x
- Các thư viện trong `requirements.txt`
- `firebase-adminsdk.json` nếu dùng Firebase cho authentication

## ⚙️ Cài đặt

```bash
git clone https://github.com/ThasiHoaf/Lab-2
cd Lab-2
pip install -r requirements.txt 
```

## ▶️ Chạy ứng dụng

1. Chạy backend:

```bash
uvicorn backend.app.main:app --reload
```

2. Trong cửa sổ khác, chạy frontend:

```bash
streamlit run frontend/app.py
```

3. Mở trình duyệt tới địa chỉ:

- Backend: `http://127.0.0.1:8000`
- Streamlit: `http://localhost:8501`

## 🔧 Cấu hình Google Login

Nếu muốn dùng tính năng đăng nhập Google, hãy thêm `google-login` vào secrets của Streamlit hoặc cấu hình tương ứng trong file cấu hình:

- `st.secrets["google-login"]` phải chứa `google-url`
- `frontend/app.py` sẽ sử dụng URL này để chuyển hướng đăng nhập

## 💡 Gợi ý phát triển

- Thay đổi model phân tích ảnh trong `backend/app/services`
- Thêm API `analyze_image` cho nhiều loại phân tích hơn
- Mở rộng frontend với phần quản lý lịch sử và thống kê
- Kết nối với cơ sở dữ liệu để lưu thông tin người dùng và kết quả phân tích

## 📚 Tài liệu tham khảo

- FastAPI
- Streamlit
- DeepFace / TensorFlow
- Firebase Authentication

## Video hướng dẫn
[Link]("https://drive.google.com/file/d/1IiTvyugKPNNGmsAVbPwNk6Iv_HCQmwPq/view?usp=sharing")