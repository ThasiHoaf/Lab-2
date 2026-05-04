import streamlit as st
import requests
from PIL import Image
import io
import pandas as pd

# Cấu hình URL của Backend FastAPI
API_URL = "http://localhost:8000/api/v1/analyze/"

# Cấu hình trang Streamlit
st.set_page_config(page_title="AI Nhận Diện Khuôn Mặt", page_icon="👤", layout="centered")

# Thêm Sidebar để người dùng nhập Token xác thực
with st.sidebar:
    st.header("🔑 Xác thực")
    auth_token = st.text_input("Nhập JWT Token (Firebase)", type="password", help="Vui lòng nhập Token hợp lệ để sử dụng API")

# Chia giao diện thành các tab
tab1, tab2 = st.tabs(["📸 Phân tích ảnh", "🕒 Lịch sử phân tích"])

with tab1:
    st.title("Phân tích Độ tuổi & Giới tính")
    st.write("Vui lòng tải lên một bức ảnh chân dung để hệ thống AI của chúng tôi phân tích.")

    uploaded_file = st.file_uploader("Chọn một bức ảnh (JPG, PNG, JPEG)", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Ảnh bạn đã tải lên", use_container_width=True)
        
        if st.button("Phân tích hình ảnh", type="primary"):
            with st.spinner("Hệ thống đang chạy mô hình Deep Learning..."):
                try:
                    img_to_send = Image.open(uploaded_file)
                    if img_to_send.mode != 'RGB':
                        img_to_send = img_to_send.convert('RGB')
                    img_to_send.thumbnail((500, 500)) 
                    
                    img_byte_arr = io.BytesIO()
                    img_to_send.save(img_byte_arr, format='JPEG', quality=85)
                    img_byte_arr.seek(0)

                    files = {"file": ("image.jpg", img_byte_arr.getvalue(), "image/jpeg")}

                    # Đính kèm token vào Request Header
                    headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
                    response = requests.post(API_URL, files=files, headers=headers, timeout=600)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("Phân tích hoàn tất!")
                        
                        col1, col2, col3 = st.columns(3)
                        col1.metric(label="Giới tính", value=result.get("gender", "N/A"))
                        col2.metric(label="Độ tuổi dự đoán", value=f"{result.get('age', 0)} tuổi")
                        confidence = result.get('confidence', 0) * 100
                        col3.metric(label="Độ tin cậy", value=f"{confidence:.1f}%")
                    else:
                        st.error(f"Lỗi từ máy chủ: {response.json().get('detail')}")
                        
                except Exception as e:
                    st.error(f"Lỗi kết nối Backend. Hãy đảm bảo FastAPI đang chạy ở port 8000.\nChi tiết: {e}")

with tab2:
    st.title("Lịch sử các lần phân tích")
    if st.button("🔄 Tải lại lịch sử"):
        try:
            # Đính kèm token vào Request Header
            headers = {"Authorization": f"Bearer {auth_token}"} if auth_token else {}
            res = requests.get(f"{API_URL}history", headers=headers)
            if res.status_code == 200:
                history_data = res.json()
                if history_data:
                    df = pd.DataFrame(history_data)
                    # Format lại bảng sử dụng thư viện Pandas cho gọn gàng
                    df.rename(columns={
                        "timestamp": "Thời gian", 
                        "gender": "Giới tính", 
                        "age": "Độ tuổi", 
                        "confidence": "Độ tin cậy"
                    }, inplace=True)
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("Chưa có dữ liệu lịch sử.")
            else:
                st.error("Không thể lấy dữ liệu từ máy chủ.")
        except Exception as e:
            st.error(f"Lỗi kết nối Backend: {e}")