import os
from datetime import datetime

from flask import current_app

from database.models import Report
from config.database import db


class ReportService:
    @staticmethod
    def generate_report(user_id, prediction, confidence, extracted_text):
        report_folder = current_app.config["REPORT_FOLDER"]
        os.makedirs(report_folder, exist_ok=True)

        from datetime import timezone
        timestamp = int(datetime.now(timezone.utc).timestamp())
        filename = f"report_{user_id}_{timestamp}.pdf"
        report_path = os.path.join(report_folder, filename)

        try:
            # Lazy import to avoid reportlab (and its deprecation warnings) during app import/tests.
            import warnings

            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message=r"ast\\.NameConstant is deprecated.*",
                    category=DeprecationWarning,
                )

                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer  # type: ignore
                from reportlab.lib.styles import getSampleStyleSheet  # type: ignore

                document = SimpleDocTemplate(report_path)
                styles = getSampleStyleSheet()

                content = []
                content.append(Paragraph("VisionAI Pro Report", styles["Title"]))
                content.append(Spacer(1, 20))
                content.append(Paragraph(f"Prediction: {prediction}", styles["Normal"]))
                content.append(Paragraph(f"Confidence: {confidence}%", styles["Normal"]))
                content.append(Paragraph("OCR Result:", styles["Heading2"]))
                content.append(
                    Paragraph(
                        extracted_text or "No text extracted.",
                        styles["BodyText"],
                    )
                )

                document.build(content)
        except Exception:
            fallback_path = os.path.join(report_folder, f"report_{user_id}_{timestamp}.txt")
            with open(fallback_path, "w", encoding="utf-8") as handle:
                handle.write(
                    "VisionAI Pro Report\n"
                    f"Prediction: {prediction}\n"
                    f"Confidence: {confidence}%\n"
                    f"OCR Result:\n{extracted_text or 'No text extracted.'}\n"
                )
            report_path = fallback_path
            filename = os.path.basename(report_path)

        report_record = Report(
            user_id=user_id,
            report_name=filename,
            report_path=report_path,
        )

        try:
            db.session.add(report_record)
            db.session.commit()
        except Exception:
            db.session.rollback()

        return report_record
