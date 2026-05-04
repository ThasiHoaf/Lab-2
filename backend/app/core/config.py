from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Cấu hình để Pydantic đọc file .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

    # Google OAuth
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    # Firebase Admin SDK
    firebase_admin_type: str
    firebase_admin_project_id: str
    firebase_admin_private_key_id: str
    firebase_admin_private_key: str
    firebase_admin_client_email: str
    firebase_admin_client_id: str
    firebase_admin_auth_uri: str
    firebase_admin_token_uri: str
    firebase_admin_auth_provider_x509_cert_url: str
    firebase_admin_client_x509_cert_url: str

    # Other app settings
    frontend_url: str
    cookie_secure: bool = False

    def get_firebase_admin_creds(self) -> dict:
        """Trả về dictionary chứa credentials cho Firebase Admin SDK."""
        # Khôi phục các ký tự xuống dòng trong private key (nếu đọc từ file .env)
        private_key = self.firebase_admin_private_key.replace('\\n', '\n')
        return {
            "type": self.firebase_admin_type,
            "project_id": self.firebase_admin_project_id,
            "private_key_id": self.firebase_admin_private_key_id,
            "private_key": private_key,
            "client_email": self.firebase_admin_client_email,
            "client_id": self.firebase_admin_client_id,
            "auth_uri": self.firebase_admin_auth_uri,
            "token_uri": self.firebase_admin_token_uri,
            "auth_provider_x509_cert_url": self.firebase_admin_auth_provider_x509_cert_url,
            "client_x509_cert_url": self.firebase_admin_client_x509_cert_url,
        }

# Tạo một đối tượng settings duy nhất để sử dụng trong toàn bộ ứng dụng
settings = Settings()