import os

class DefaultConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///./barangay_requests_tracker.db"
    DIGEST_SALT = os.getenv("DIGEST_SALT")
    API_KEY = os.getenv("X_API_KEY")
    BRGY_CODE = os.getenv("X_BRGY_CODE")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
