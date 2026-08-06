from sqlalchemy import func

from database.models import (
    Prediction,
    OCRResult,
    DetectionResult,
    Report,
    ActivityLog
)


class AnalyticsService:

    @staticmethod
    def get_dashboard_stats(user_id):

        total_predictions = Prediction.query.filter_by(
            user_id=user_id
        ).count()

        total_ocr = OCRResult.query.filter_by(
            user_id=user_id
        ).count()

        total_detections = DetectionResult.query.filter_by(
            user_id=user_id
        ).count()

        total_reports = Report.query.filter_by(
            user_id=user_id
        ).count()

        return {
            "total_predictions": total_predictions,
            "total_ocr": total_ocr,
            "total_detections": total_detections,
            "total_reports": total_reports
        }

    @staticmethod
    def get_prediction_history(
        user_id,
        prediction_type=None,
        from_date=None,
        to_date=None,
        min_confidence=None,
        search_text=None
    ):

        query = (
            Prediction.query
            .filter_by(user_id=user_id)
        )

        if from_date:
            query = query.filter(Prediction.created_at >= from_date)

        if to_date:
            query = query.filter(Prediction.created_at <= to_date)

        if min_confidence is not None:
            query = query.filter(Prediction.confidence >= float(min_confidence))

        # prediction_type currently maps to the stored Prediction.prediction label
        if prediction_type:
            query = query.filter(Prediction.prediction == prediction_type)

        if search_text:
            # Best-effort search only within prediction labels for now
            query = query.filter(Prediction.prediction.ilike(f"%{search_text}%"))

        return (
            query
            .order_by(Prediction.created_at.desc())
            .all()
        )

    @staticmethod
    def log_activity(user_id, action, details=None):
        log_entry = ActivityLog(
            user_id=user_id,
            action=action,
            details=details,
        )
        from config.database import db

        try:
            db.session.add(log_entry)
            db.session.commit()
        except Exception:
            db.session.rollback()

    @staticmethod
    def get_recent_activity(user_id, limit=10):
        return (
            ActivityLog.query.filter_by(user_id=user_id)
            .order_by(ActivityLog.created_at.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_top_predictions(user_id):

        results = (
            Prediction.query
            .with_entities(
                Prediction.prediction,
                func.count(Prediction.id)
            )
            .filter_by(user_id=user_id)
            .group_by(Prediction.prediction)
            .all()
        )

        labels = []
        values = []

        for prediction, count in results:
            labels.append(prediction)
            values.append(count)

        return {
            "labels": labels,
            "values": values
        }