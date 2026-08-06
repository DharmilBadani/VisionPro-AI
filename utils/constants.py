"""
Application-wide constants.
"""

from pathlib import Path

PROJECT_NAME = "VisionAI Pro"
PROJECT_VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent.parent

SUPPORTED_IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "webp"
}

MAX_TOP_PREDICTIONS = 5

IMAGE_SIZE = (224, 224)

DEFAULT_CONFIDENCE_THRESHOLD = 0.50

DEFAULT_TIMEZONE = "UTC"

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | "
    "%(name)s | %(filename)s:%(lineno)d | %(message)s"
)

CLASSIFICATION_MODEL_NAME = "MobileNetV2"

YOLO_MODEL_NAME = "YOLOv8n"

REPORT_TITLE = "VisionAI Prediction Report"

API_VERSION = "v1"

STATUS_SUCCESS = "success"

STATUS_ERROR = "error"

STATUS_WARNING = "warning"

USER_ROLE = "user"

ADMIN_ROLE = "admin"

UPLOAD_SUBDIRECTORY = "uploads"

PREDICTION_SUBDIRECTORY = "predictions"

REPORT_SUBDIRECTORY = "reports"

IMAGE_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}