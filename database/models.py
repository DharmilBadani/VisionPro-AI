from datetime import datetime, timezone

from flask_login import UserMixin

def utcnow_naive():
    return datetime.now(timezone.utc).replace(tzinfo=None)

from config.database import (
    db,
    login_manager
)


@login_manager.user_loader
def load_user(user_id):

    try:
        return User.query.get(
            int(user_id)
        )
    except Exception:
        return None


class User(
    UserMixin,
    db.Model
):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user"
    )

    is_active_user = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=utcnow_naive
    )

    updated_at = db.Column(
        db.DateTime,
        default=utcnow_naive,
        onupdate=utcnow_naive
    )

    @property
    def is_active(self):
        return self.is_active_user


class Prediction(db.Model):

    __tablename__ = "predictions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    image_name = db.Column(
        db.String(255),
        nullable=False
    )

    image_path = db.Column(
        db.String(500),
        nullable=False
    )

    prediction = db.Column(
        db.String(255),
        nullable=False
    )

    confidence = db.Column(
        db.Float,
        nullable=False
    )

    model_used = db.Column(
        db.String(100),
        default="MobileNetV2"
    )

    created_at = db.Column(
        db.DateTime,
        default=utcnow_naive
    )


class DetectionResult(db.Model):

    __tablename__ = "detection_results"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    image_path = db.Column(
        db.String(500),
        nullable=False
    )

    detected_objects = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=utcnow_naive
    )


class OCRResult(db.Model):

    __tablename__ = "ocr_results"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    image_path = db.Column(
        db.String(500),
        nullable=False
    )

    extracted_text = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=utcnow_naive
    )


class CaptionResult(db.Model):

    __tablename__ = "caption_results"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    image_path = db.Column(
        db.String(500),
        nullable=False
    )

    generated_caption = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=utcnow_naive
    )


class Report(db.Model):

    __tablename__ = "reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    report_name = db.Column(
        db.String(255),
        nullable=False
    )

    report_path = db.Column(
        db.String(500),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=utcnow_naive
    )


class ActivityLog(db.Model):

    __tablename__ = "activity_logs"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    action = db.Column(
        db.String(255),
        nullable=False
    )

    details = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=utcnow_naive
    )