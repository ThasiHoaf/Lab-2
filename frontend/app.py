import streamlit as st
import requests
from PIL import Image
import io
import pandas as pd

from api_client import signup, login, google_login, analyze_image, get_analysis_history

st.set_page_config(page_title="AI Nhận Diện Khuôn Mặt", page_icon="👤", layout="centered")

if "user" not in st.session_state:
    st.session_state.user = None

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

if "show_login" not in st.session_state:
    st.session_state.show_login = True


def clear_google_query_params():
    try:
        st.query_params.clear()
    except Exception:
        pass


def handle_google_login_callback():
    if st.session_state.user:
        return

    params = st.query_params
    raw_token = params.get("id_token")

    if not raw_token:
        return

    id_token = raw_token[0] if isinstance(raw_token, list) else raw_token

    try:
        user = google_login(id_token)
        st.session_state.user = user
        clear_google_query_params()
        st.success("Đăng nhập Google thành công")
        st.rerun()
    except requests.HTTPError as e:
        st.error(f"Đăng nhập Google thất bại: {e}")
        clear_google_query_params()
    except Exception as e:
        st.error(f"Lỗi xử lý Google login: {e}")
        clear_google_query_params()


def login_form():
    st.subheader("Đăng nhập")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        submitted = st.form_submit_button("Đăng nhập")
        goto_signup = st.form_submit_button("Chưa có tài khoản? Đăng ký")

    if goto_signup:
        st.session_state.show_signup = True
        st.session_state.show_login = False
        st.rerun()

    if submitted:
        try:
            user = login(email, password)
            st.session_state.user = user
            st.success("Đăng nhập thành công")
            st.rerun()
        except requests.HTTPError as e:
            st.error(f"Đăng nhập thất bại: {e}")
        except Exception as e:
            st.error(f"Lỗi đăng nhập: {e}")

    st.markdown("### Hoặc")

    google_login_url = dict(st.secrets["google-login"])["google-url"]

    if google_login_url:
        st.markdown(
        f'''
        <a href="{google_login_url}" target="_self" style="
            display: inline-block;
            width: 100%;
            text-align: center;
            padding: 0.6rem 1rem;
            background-color: white;
            color: black;
            text-decoration: none;
            border-radius: 0.5rem;
            border: 1px solid #ddd;
            font-weight: 600;
        ">
            Đăng nhập với Google
        </a>
        ''',
        unsafe_allow_html=True,
    )
    else:
        st.info(
            "Chưa cấu hình Google-login trong secrets. "
            "Hãy thêm URL đăng nhập Google để dùng tính năng này."
        )


def signup_form():
    st.subheader("Đăng ký")
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        submitted = st.form_submit_button("Tạo tài khoản")
        goto_login = st.form_submit_button("Đã có tài khoản? Đăng nhập")

    if goto_login:
        st.session_state.show_signup = False
        st.session_state.show_login = True
        st.rerun()

    if submitted:
        try:
            signup(email, password)
            st.success("Tạo tài khoản thành công, hãy đăng nhập")
            st.session_state.show_signup = False
            st.session_state.show_login = True
            st.rerun()
        except requests.HTTPError as e:
            st.error(f"Đăng ký thất bại: {e}")
        except Exception as e:
            st.error(f"Lỗi đăng ký: {e}")


handle_google_login_callback()

st.title("📸 Phân tích Độ tuổi & Giới tính")

if st.session_state.user:
    st.success(f"👤 Đang đăng nhập: **{st.session_state.user.get('email', 'Người dùng')}**")
    if st.button("Đăng xuất", type="primary"):
        st.session_state.user = None
        clear_google_query_params()
        st.rerun()
else:
    if st.session_state.show_signup:
        signup_form()
    else:
        login_form()

st.divider()

if st.session_state.user:
    tab1, tab2 = st.tabs(["📸 Phân tích ảnh", "🕒 Lịch sử phân tích"])
    
    with tab1:
        st.write("Vui lòng tải lên một bức ảnh chân dung để hệ thống AI của chúng tôi phân tích.")

        # Widget tải file
        uploaded_file = st.file_uploader("Chọn một bức ảnh (JPG, PNG, JPEG)", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None:
            # Hiển thị ảnh cho người dùng xem trước
            image = Image.open(uploaded_file)
            st.image(image, caption="Ảnh bạn đã tải lên", use_container_width=True)
            
            # Nút bấm bắt đầu phân tích
            if st.button("Phân tích hình ảnh", type="primary"):
                with st.spinner("Hệ thống đang chạy mô hình Deep Learning..."):
                    try:
                        # 1. Tiền xử lý: Nén và thu nhỏ ảnh để giảm tải và tăng tốc độ phân tích
                        img_to_send = Image.open(uploaded_file)
                        if img_to_send.mode != 'RGB':
                            img_to_send = img_to_send.convert('RGB')
                        img_to_send.thumbnail((500, 500)) # Thu nhỏ ảnh tối đa 500x500px
                        
                        img_byte_arr = io.BytesIO()
                        img_to_send.save(img_byte_arr, format='JPEG', quality=85)
                        
                        # Gửi file tới Backend thông qua api_client
                        result = analyze_image(
                            file_bytes=img_byte_arr.getvalue(),
                            filename="image.jpg",
                            content_type="image/jpeg",
                            id_token=st.session_state.user.get("idToken")
                        )
                        
                        st.success("Phân tích hoàn tất!")
                        col1, col2, col3 = st.columns(3)
                        col1.metric(label="Giới tính", value=result.get("gender", "N/A"))
                        col2.metric(label="Độ tuổi dự đoán", value=f"{result.get('age', 0)} tuổi")
                        
                        confidence = result.get('confidence', 0) * 100
                        col3.metric(label="Độ tin cậy", value=f"{confidence:.1f}%")
                    except requests.HTTPError as e:
                        st.error(f"Lỗi phản hồi từ máy chủ: Vui lòng đảm bảo bạn tải lên tệp ảnh hợp lệ có khuôn mặt.")
                    except Exception as e:
                        st.error(f"Lỗi kết nối: {e}")

    with tab2:
        st.title("Lịch sử các lần phân tích")
        if st.button("🔄 Tải lại lịch sử"):
            try:
                # ✅ Sử dụng hàm api_client với xác thực
                history_data = get_analysis_history(st.session_state.user.get("idToken"))
                if history_data:
                    df = pd.DataFrame(history_data)
                    df.rename(columns={
                        "timestamp": "Thời gian", 
                        "gender": "Giới tính", 
                        "age": "Độ tuổi", 
                        "confidence": "Độ tin cậy"
                    }, inplace=True)
                    st.dataframe(df, use_container_width=True)
                    st.success(f"✅ Tải thành công {len(history_data)} bản ghi!")
                else:
                    st.info("Chưa có dữ liệu lịch sử.")
            except requests.HTTPError as e:
                if e.response.status_code == 401:
                    st.error("❌ Vui lòng đăng nhập lại!")
                else:
                    st.error(f"❌ Lỗi từ máy chủ: {e}")
            except Exception as e:
                st.error(f"❌ Lỗi kết nối: {e}")
else:
    st.info("Vui lòng đăng nhập để sử dụng tính năng phân tích hình ảnh.")