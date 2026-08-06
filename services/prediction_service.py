import json

from config.database import db
from database.models import DetectionResult, OCRResult, Prediction
from services.notifications import send_notification
from services.analytics_service import AnalyticsService


class PredictionService:
    """Prediction service with lazy model initialization.

    Heavy ML frameworks are imported and initialized only when endpoints are invoked.
    """

    _classifier = None
    _detector = None
    _ocr_engine = None

    @classmethod
    def _get_classifier(cls):
        if cls._classifier is None:
            from ai_models.classifier import ImageClassifier

            cls._classifier = ImageClassifier()
        return cls._classifier

    @classmethod
    def _get_detector(cls):
        if cls._detector is None:
            from ai_models.detector import ObjectDetector

            cls._detector = ObjectDetector()
        return cls._detector

    @classmethod
    def _get_ocr(cls):
        if cls._ocr_engine is None:
            from ai_models.ocr_engine import OCREngine

            cls._ocr_engine = OCREngine()
        return cls._ocr_engine

    @staticmethod
    def classify_image(user_id, image_name, image_path, model_name="mobilenet_v2"):
        if image_path.lower().endswith(".pdf"):
            predictions = [{"label": "pdf_document", "confidence": 100.0}]
        else:
            classifier = PredictionService._get_classifier()
            predictions = classifier.predict(image_path, model_name=model_name)
        best_prediction = predictions[0]

        record = Prediction(
            user_id=user_id,
            image_name=image_name,
            image_path=image_path,
            prediction=best_prediction["label"],
            confidence=best_prediction["confidence"],
            model_used=model_name,
        )

        try:
            db.session.add(record)
            db.session.commit()
        except Exception:
            db.session.rollback()

        AnalyticsService.log_activity(user_id, "prediction_completed", f"Prediction ({model_name}): {best_prediction['label']}")

        return {
            "prediction": best_prediction,
            "top_predictions": predictions,
        }

    @staticmethod
    def detect_objects(user_id, image_path, output_path=None):
        if image_path.lower().endswith(".pdf"):
            detections = []
        else:
            detector = PredictionService._get_detector()
            detections = detector.detect(image_path, output_path=output_path)

        record = DetectionResult(
            user_id=user_id,
            image_path=image_path,
            detected_objects=json.dumps(detections),
        )

        try:
            db.session.add(record)
            db.session.commit()
        except Exception:
            db.session.rollback()

        AnalyticsService.log_activity(user_id, "detection_completed", f"Detected {len(detections)} objects")
        return detections

    @staticmethod
    def extract_text(user_id, image_path):
        if image_path.lower().endswith(".pdf"):
            import pypdf
            try:
                reader = pypdf.PdfReader(image_path)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                text = text.strip()
                if not text:
                    text = "No selectable text found in the PDF document."
            except Exception as e:
                text = f"Error extracting text from PDF: {str(e)}"
        else:
            ocr_engine = PredictionService._get_ocr()
            text = ocr_engine.extract_text(image_path)

        record = OCRResult(
            user_id=user_id,
            image_path=image_path,
            extracted_text=text,
        )

        try:
            db.session.add(record)
            db.session.commit()
        except Exception:
            db.session.rollback()

        AnalyticsService.log_activity(user_id, "ocr_completed", "OCR text extracted")
        return text

    @staticmethod
    def generate_and_save_caption(user_id, image_path, label, confidence, detections):
        from ai_models.image_caption import ImageCaptioner
        from database.models import CaptionResult

        caption = ImageCaptioner.generate_caption(label, confidence, detections)

        record = CaptionResult(
            user_id=user_id,
            image_path=image_path,
            generated_caption=caption
        )

        try:
            db.session.add(record)
            db.session.commit()
        except Exception:
            db.session.rollback()

        AnalyticsService.log_activity(user_id, "caption_generated", "Visual caption generated")
        return caption
