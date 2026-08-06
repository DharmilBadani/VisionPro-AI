import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "visionai-secret-key"
    )

    _db_url = os.getenv("DATABASE_URL", "sqlite:///visionai.db")
    if _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _db_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAX_CONTENT_LENGTH = int(
        os.getenv(
            "MAX_CONTENT_LENGTH",
            16777216
        )
    )

    UPLOAD_FOLDER = os.getenv(
        "UPLOAD_FOLDER",
        "static/uploads"
    )

    REPORT_FOLDER = os.getenv(
        "REPORT_FOLDER",
        "static/reports"
    )

    ALLOWED_EXTENSIONS = {
        "jpg",
        "jpeg",
        "png",
        "webp",
        "pdf"
    }

    # Flask-Login session behavior:
    # User must be logged out by default when the browser/window is closed.
    # (Session cookies are non-permanent by default.)
    SESSION_PERMANENT = False
