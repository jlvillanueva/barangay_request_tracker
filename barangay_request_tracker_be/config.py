import os

class DefaultConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///./barangay_requests_tracker.db"
    DIGEST_SALT = os.getenv("DIGEST_SALT")
