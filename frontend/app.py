# import streamlit as st
# import requests
# from PIL import Image
# import io
# import pandas as pd

# from api_client import signup, login, google_login, analyze_image, get_analysis_history

# st.set_page_config(page_title="AI Nhận Diện Khuôn Mặt", page_icon="👤", layout="centered")

# if "user" not in st.session_state:
#     st.session_state.user = None

# if "show_signup" not in st.session_state:
#     st.session_state.show_signup = False

# if "show_login" not in st.session_state:
#     st.session_state.show_login = True


# def clear_google_query_params():
#     try:
#         st.query_params.clear()
#     except Exception:
#         pass


# def handle_google_login_callback():
#     if st.session_state.user:
#         return

#     params = st.query_params
#     raw_token = params.get("id_token")

#     if not raw_token:
#         return

#     id_token = raw_token[0] if isinstance(raw_token, list) else raw_token

#     try:
#         user = google_login(id_token)
#         st.session_state.user = user
#         clear_google_query_params()
#         st.success("Đăng nhập Google thành công")
#         st.rerun()
#     except requests.HTTPError as e:
#         st.error(f"Đăng nhập Google thất bại: {e}")
#         clear_google_query_params()
#     except Exception as e:
#         st.error(f"Lỗi xử lý Google login: {e}")
#         clear_google_query_params()


# def login_form():
#     st.subheader("Đăng nhập")

#     with st.form("login_form"):
#         email = st.text_input("Email")
#         password = st.text_input("Mật khẩu", type="password")
#         submitted = st.form_submit_button("Đăng nhập")
#         goto_signup = st.form_submit_button("Chưa có tài khoản? Đăng ký")

#     if goto_signup:
#         st.session_state.show_signup = True
#         st.session_state.show_login = False
#         st.rerun()

#     if submitted:
#         try:
#             user = login(email, password)
#             st.session_state.user = user
#             st.success("Đăng nhập thành công")
#             st.rerun()
#         except requests.HTTPError as e:
#             st.error(f"Đăng nhập thất bại: {e}")
#         except Exception as e:
#             st.error(f"Lỗi đăng nhập: {e}")

#     st.markdown("### Hoặc")

#     google_login_url = dict(st.secrets["google-login"])["google-url"]

#     if google_login_url:
#         st.markdown(
#         f'''
#         <a href="{google_login_url}" target="_self" style="
#             display: inline-block;
#             width: 100%;
#             text-align: center;
#             padding: 0.6rem 1rem;
#             background-color: white;
#             color: black;
#             text-decoration: none;
#             border-radius: 0.5rem;
#             border: 1px solid #ddd;
#             font-weight: 600;
#         ">
#             Đăng nhập với Google
#         </a>
#         ''',
#         unsafe_allow_html=True,
#     )
#     else:
#         st.info(
#             "Chưa cấu hình Google-login trong secrets. "
#             "Hãy thêm URL đăng nhập Google để dùng tính năng này."
#         )


# def signup_form():
#     st.subheader("Đăng ký")
#     with st.form("signup_form"):
#         email = st.text_input("Email")
#         password = st.text_input("Mật khẩu", type="password")
#         submitted = st.form_submit_button("Tạo tài khoản")
#         goto_login = st.form_submit_button("Đã có tài khoản? Đăng nhập")

#     if goto_login:
#         st.session_state.show_signup = False
#         st.session_state.show_login = True
#         st.rerun()

#     if submitted:
#         try:
#             signup(email, password)
#             st.success("Tạo tài khoản thành công, hãy đăng nhập")
#             st.session_state.show_signup = False
#             st.session_state.show_login = True
#             st.rerun()
#         except requests.HTTPError as e:
#             st.error(f"Đăng ký thất bại: {e}")
#         except Exception as e:
#             st.error(f"Lỗi đăng ký: {e}")


# handle_google_login_callback()

# st.title("📸 Phân tích Độ tuổi & Giới tính")

# if st.session_state.user:
#     st.success(f"👤 Đang đăng nhập: **{st.session_state.user.get('email', 'Người dùng')}**")
#     if st.button("Đăng xuất", type="primary"):
#         st.session_state.user = None
#         clear_google_query_params()
#         st.rerun()
# else:
#     if st.session_state.show_signup:
#         signup_form()
#     else:
#         login_form()

# st.divider()

# if st.session_state.user:
#     tab1, tab2 = st.tabs(["📸 Phân tích ảnh", "🕒 Lịch sử phân tích"])
    
#     with tab1:
#         st.write("Vui lòng tải lên một bức ảnh chân dung để hệ thống AI của chúng tôi phân tích.")

#         # Widget tải file
#         uploaded_file = st.file_uploader("Chọn một bức ảnh (JPG, PNG, JPEG)", type=["jpg", "jpeg", "png"])

#         if uploaded_file is not None:
#             # Hiển thị ảnh cho người dùng xem trước
#             image = Image.open(uploaded_file)
#             st.image(image, caption="Ảnh bạn đã tải lên", use_container_width=True)
            
#             # Nút bấm bắt đầu phân tích
#             if st.button("Phân tích hình ảnh", type="primary"):
#                 with st.spinner("Hệ thống đang chạy mô hình Deep Learning..."):
#                     try:
#                         # 1. Tiền xử lý: Nén và thu nhỏ ảnh để giảm tải và tăng tốc độ phân tích
#                         img_to_send = Image.open(uploaded_file)
#                         if img_to_send.mode != 'RGB':
#                             img_to_send = img_to_send.convert('RGB')
#                         img_to_send.thumbnail((500, 500)) # Thu nhỏ ảnh tối đa 500x500px
                        
#                         img_byte_arr = io.BytesIO()
#                         img_to_send.save(img_byte_arr, format='JPEG', quality=85)
                        
#                         # Gửi file tới Backend thông qua api_client
#                         result = analyze_image(
#                             file_bytes=img_byte_arr.getvalue(),
#                             filename="image.jpg",
#                             content_type="image/jpeg",
#                             id_token=st.session_state.user.get("idToken")
#                         )
                        
#                         st.success("Phân tích hoàn tất!")
#                         col1, col2, col3 = st.columns(3)
#                         col1.metric(label="Giới tính", value=result.get("gender", "N/A"))
#                         col2.metric(label="Độ tuổi dự đoán", value=f"{result.get('age', 0)} tuổi")
                        
#                         confidence = result.get('confidence', 0) * 100
#                         col3.metric(label="Độ tin cậy", value=f"{confidence:.1f}%")
#                     except requests.HTTPError as e:
#                         st.error(f"Lỗi phản hồi từ máy chủ: Vui lòng đảm bảo bạn tải lên tệp ảnh hợp lệ có khuôn mặt.")
#                     except Exception as e:
#                         st.error(f"Lỗi kết nối: {e}")

#     with tab2:
#         st.title("Lịch sử các lần phân tích")
#         if st.button("🔄 Tải lại lịch sử"):
#             try:
#                 # ✅ Sử dụng hàm api_client với xác thực
#                 history_data = get_analysis_history(st.session_state.user.get("idToken"))
#                 if history_data:
#                     df = pd.DataFrame(history_data)
#                     df.rename(columns={
#                         "timestamp": "Thời gian", 
#                         "gender": "Giới tính", 
#                         "age": "Độ tuổi", 
#                         "confidence": "Độ tin cậy"
#                     }, inplace=True)
#                     st.dataframe(df, use_container_width=True)
#                     st.success(f"✅ Tải thành công {len(history_data)} bản ghi!")
#                 else:
#                     st.info("Chưa có dữ liệu lịch sử.")
#             except requests.HTTPError as e:
#                 if e.response.status_code == 401:
#                     st.error("❌ Vui lòng đăng nhập lại!")
#                 else:
#                     st.error(f"❌ Lỗi từ máy chủ: {e}")
#             except Exception as e:
#                 st.error(f"❌ Lỗi kết nối: {e}")
# else:
#     st.info("Vui lòng đăng nhập để sử dụng tính năng phân tích hình ảnh.")

import streamlit as st
import requests
from PIL import Image
import io
import pandas as pd

from api_client import signup, login, google_login, analyze_image, get_analysis_history

# 1. CẤU HÌNH TRANG VÀ THÊM CUSTOM CSS (Đưa lên đầu tiên)
st.set_page_config(page_title="AI Facial Analysis", page_icon="🧬", layout="wide")

def inject_custom_css():
    st.markdown("""
        <style>
            /* Căn giữa form đăng nhập */
            .auth-container {
                max-width: 400px;
                margin: 0 auto;
                padding: 2rem;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            /* Làm đẹp các thẻ Metric (Kết quả hiển thị) */
            div[data-testid="metric-container"] {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                padding: 5% 10%;
                border-radius: 12px;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s;
            }
            div[data-testid="metric-container"]:hover {
                transform: translateY(-2px);
                box-shadow: 2px 5px 15px rgba(0, 0, 0, 0.1);
            }
            /* Dark mode support cho metric */
            @media (prefers-color-scheme: dark) {
                div[data-testid="metric-container"] {
                    background-color: #262730;
                    border: 1px solid #333;
                }
            }
            /* Tùy chỉnh nút Google */
            .google-btn {
                display: inline-block;
                width: 100%;
                text-align: center;
                padding: 0.6rem 1rem;
                background-color: #ffffff;
                color: #444;
                text-decoration: none;
                border-radius: 8px;
                border: 1px solid #ddd;
                font-weight: 600;
                box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                transition: background-color 0.2s;
            }
            .google-btn:hover {
                background-color: #f8f9fa;
                color: #000;
            }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# --- KHỞI TẠO SESSION STATE ---
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
        st.rerun()
    except requests.HTTPError as e:
        st.error(f"Đăng nhập Google thất bại: {e}")
        clear_google_query_params()
    except Exception as e:
        st.error(f"Lỗi xử lý Google login: {e}")
        clear_google_query_params()

# --- GIAO DIỆN XÁC THỰC (Được căn giữa) ---
def login_form():
    col1, col2, col3 = st.columns([1, 2, 1]) # Sử dụng cột để căn giữa
    with col2:
        st.markdown("<h2 style='text-align: center; color: #1E88E5;'>Đăng Nhập Hệ Thống</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: gray;'>Truy cập công cụ phân tích AI của bạn</p>", unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("📧 Email")
            password = st.text_input("🔑 Mật khẩu", type="password")
            submitted = st.form_submit_button("Đăng nhập", use_container_width=True)
            goto_signup = st.form_submit_button("Chưa có tài khoản? Đăng ký ngay", use_container_width=True)

        if goto_signup:
            st.session_state.show_signup = True
            st.session_state.show_login = False
            st.rerun()

        if submitted:
            try:
                user = login(email, password)
                st.session_state.user = user
                st.rerun()
            except requests.HTTPError as e:
                st.error(f"Đăng nhập thất bại: {e}")
            except Exception as e:
                st.error(f"Lỗi hệ thống: {e}")

        st.markdown("<div style='text-align: center; margin: 15px 0;'><b>— Hoặc —</b></div>", unsafe_allow_html=True)
        google_login_url = dict(st.secrets.get("google-login", {})).get("google-url", None)

        if google_login_url:
            st.markdown(f'<a href="{google_login_url}" target="_self" class="google-btn">🌐 Đăng nhập với Google</a>', unsafe_allow_html=True)
        else:
            st.info("Chưa cấu hình Google-login.")

def signup_form():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center; color: #1E88E5;'>Tạo Tài Khoản</h2>", unsafe_allow_html=True)
        with st.form("signup_form"):
            email = st.text_input("📧 Email")
            password = st.text_input("🔑 Mật khẩu", type="password")
            submitted = st.form_submit_button("Tạo tài khoản", use_container_width=True)
            goto_login = st.form_submit_button("Đã có tài khoản? Trở về Đăng nhập", use_container_width=True)

        if goto_login:
            st.session_state.show_signup = False
            st.session_state.show_login = True
            st.rerun()

        if submitted:
            try:
                signup(email, password)
                st.success("Tạo tài khoản thành công! Vui lòng đăng nhập.")
                st.session_state.show_signup = False
                st.session_state.show_login = True
            except requests.HTTPError as e:
                st.error(f"Đăng ký thất bại: {e}")
            except Exception as e:
                st.error(f"Lỗi đăng ký: {e}")

handle_google_login_callback()

# --- HEADER APP ---
if st.session_state.user:
    col_title, col_user = st.columns([3, 1])
    with col_title:
        st.title("🧬 Phân Tích Khuôn Mặt AI")
    with col_user:
        st.write("") # Dịch nút xuống một chút
        st.write("")
        st.info(f"👤 **{st.session_state.user.get('email', 'User')}**")
        if st.button("Đăng xuất", type="secondary", use_container_width=True):
            st.session_state.user = None
            clear_google_query_params()
            st.rerun()
    st.divider()

    # --- MAIN CONTENT ---
    tab_analyze, tab_history = st.tabs(["📸 Trạm Phân Tích", "📊 Lịch Sử Dữ Liệu"])
    
    with tab_analyze:
        st.markdown("#### Tải lên ảnh chân dung để trích xuất đặc trưng sinh trắc học")
        
        # Bố cục 2 cột cho phần phân tích
        col_upload, col_result = st.columns([1.2, 1])
        
        with col_upload:
            st.container(border=True)
            uploaded_file = st.file_uploader("Kéo thả hoặc chọn ảnh (JPG, PNG)", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
            
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                # Hiển thị ảnh bo góc bằng CSS
                st.image(image, caption="Dữ liệu đầu vào", use_container_width=True)

        with col_result:
            if uploaded_file is not None:
                st.markdown("<br>", unsafe_allow_html=True) # Tạo khoảng trống
                if st.button("🚀 Bắt đầu Phân tích AI", type="primary", use_container_width=True):
                    with st.status("🧠 Đang xử lý qua mô hình Deep Learning...", expanded=True) as status:
                        st.write("1. Tiền xử lý & Chuẩn hóa kích thước ảnh...")
                        try:
                            img_to_send = Image.open(uploaded_file)
                            if img_to_send.mode != 'RGB':
                                img_to_send = img_to_send.convert('RGB')
                            img_to_send.thumbnail((500, 500))
                            img_byte_arr = io.BytesIO()
                            img_to_send.save(img_byte_arr, format='JPEG', quality=85)
                            
                            st.write("2. Trích xuất đặc trưng (Feature extraction)...")
                            result = analyze_image(
                                file_bytes=img_byte_arr.getvalue(),
                                filename="image.jpg",
                                content_type="image/jpeg",
                                id_token=st.session_state.user.get("idToken")
                            )
                            status.update(label="✅ Phân tích hoàn tất!", state="complete", expanded=False)
                            
                            # Hiển thị kết quả bằng các metric cards
                            st.markdown("### Kết quả Phân tích")
                            m1, m2 = st.columns(2)
                            m1.metric(label="Giới tính", value=result.get("gender", "N/A"))
                            m2.metric(label="Độ tuổi ước tính", value=f"{result.get('age', 0)} tuổi")
                            
                            confidence = result.get('confidence', 0) * 100
                            st.metric(label="Chỉ số tin cậy (Confidence Score)", value=f"{confidence:.2f}%")
                            
                            # Thanh tiến trình thể hiện độ tin cậy trực quan
                            st.progress(int(confidence) if confidence <= 100 else 100)

                        except requests.HTTPError as e:
                            status.update(label="❌ Lỗi xử lý", state="error")
                            st.error("Không tìm thấy khuôn mặt hợp lệ trong ảnh.")
                        except Exception as e:
                            status.update(label="❌ Lỗi hệ thống", state="error")
                            st.error(f"Lỗi kết nối: {e}")
            else:
                st.info("👈 Vui lòng tải ảnh lên ở cột bên trái để xem kết quả.")

    with tab_history:
        col_title_hist, col_btn_hist = st.columns([4, 1])
        with col_title_hist:
            st.subheader("Nhật ký phân tích")
        with col_btn_hist:
            refresh = st.button("🔄 Làm mới dữ liệu", use_container_width=True)

        try:
            history_data = get_analysis_history(st.session_state.user.get("idToken"))
            if history_data:
                df = pd.DataFrame(history_data)
                
                # Làm sạch và định dạng lại DataFrame để hiển thị chuyên nghiệp hơn
                df = df.rename(columns={
                    "timestamp": "Thời gian", 
                    "gender": "Giới tính", 
                    "age": "Độ tuổi", 
                    "confidence": "Độ tin cậy"
                })
                
                # Tùy chỉnh hiển thị cột
                st.dataframe(
                    df, 
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Độ tin cậy": st.column_config.NumberColumn("Độ tin cậy", format="%.2f"),
                        "Độ tuổi": st.column_config.NumberColumn("Độ tuổi", format="%d"),
                        # Nếu timestamp của bạn là chuỗi ISO, Streamlit tự nhận diện hoặc bạn có thể cast nó sang datetime
                    }
                )
                st.caption(f"Tổng số bản ghi: {len(df)}")
            else:
                st.info("📭 Chưa có dữ liệu phân tích nào được ghi nhận.")
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                st.error("❌ Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại!")
            else:
                st.error(f"❌ Lỗi từ máy chủ: {e}")
        except Exception as e:
            st.error(f"❌ Lỗi kết nối: {e}")

else:
    # Nếu chưa đăng nhập, hiển thị form ở giữa màn hình
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.session_state.show_signup:
        signup_form()
    else:
        login_form()