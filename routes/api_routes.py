from flask import (
    Blueprint,
    jsonify,
    request
)

from flask_login import (
    login_required,
    current_user
)

from services.image_service import (
    ImageService
)

from services.prediction_service import (
    PredictionService
)

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Global limiter is initialized in app.py; if not present, create a local fallback.
try:
    limiter = Limiter(key_func=get_remote_address)
except Exception:
    limiter = None

API_LIMIT = "30 per minute"






@api_bp.route(
    "/health",
    methods=["GET"]
)
def health():

    return jsonify(
        {
            "status": "success",
            "message": "VisionAI API Running"
        }
    )


@api_bp.route(
    "/classify",
    methods=["POST"]
)
@login_required
def classify():

    try:

        image_file = request.files.get(
            "image"
        )

        if not image_file:

            return jsonify(
                {
                    "status": "error",
                    "message": "Image file required."
                }
            ), 400

        image_info = (
            ImageService.save_uploaded_image(
                image_file
            )
        )

        result = (
            PredictionService.classify_image(
                current_user.id,
                image_info["filename"],
                image_info["file_path"]
            )
        )

        return jsonify(
            {
                "status": "success",
                "prediction": result[
                    "prediction"
                ],
                "top_predictions": result[
                    "top_predictions"
                ]
            }
        )

    except Exception:

        return jsonify(

            {

                "status": "error",

                "message": "Server error."

            }

        ), 500


@api_bp.route(
    "/detect",
    methods=["POST"]
)
@login_required
def detect():

    try:

        image_file = request.files.get(
            "image"
        )

        if not image_file:

            return jsonify(
                {
                    "status": "error",
                    "message": "Image file required."
                }
            ), 400

        image_info = (
            ImageService.save_uploaded_image(
                image_file
            )
        )

        detections = (
            PredictionService.detect_objects(
                current_user.id,
                image_info["file_path"]
            )
        )

        return jsonify(
            {
                "status": "success",
                "detections": detections
            }
        )

    except Exception:

        return jsonify(

            {

                "status": "error",

                "message": "Server error."

            }

        ), 500


@api_bp.route(
    "/ocr",
    methods=["POST"]
)
@login_required
def ocr():

    try:

        image_file = request.files.get(
            "image"
        )

        if not image_file:

            return jsonify(
                {
                    "status": "error",
                    "message": "Image file required."
                }
            ), 400

        image_info = (
            ImageService.save_uploaded_image(
                image_file
            )
        )

        extracted_text = (
            PredictionService.extract_text(
                current_user.id,
                image_info["file_path"]
            )
        )

        return jsonify(
            {
                "status": "success",
                "text": extracted_text
            }
        )

    except Exception:

        return jsonify(

            {

                "status": "error",

                "message": "Server error."

            }

        ), 500


@api_bp.route(
    "/analyze",
    methods=["POST"]
)
@login_required
def analyze():

    try:

        image_file = request.files.get(
            "image"
        )

        if not image_file:

            return jsonify(
                {
                    "status": "error",
                    "message": "Image file required."
                }
            ), 400

        image_info = (
            ImageService.save_uploaded_image(
                image_file
            )
        )

        classification = (
            PredictionService.classify_image(
                current_user.id,
                image_info["filename"],
                image_info["file_path"]
            )
        )

        detections = (
            PredictionService.detect_objects(
                current_user.id,
                image_info["file_path"]
            )
        )

        extracted_text = (
            PredictionService.extract_text(
                current_user.id,
                image_info["file_path"]
            )
        )

        return jsonify(
            {
                "status": "success",
                "classification": classification,
                "detections": detections,
                "ocr_text": extracted_text
            }
        )

    except Exception:

        return jsonify(

            {

                "status": "error",

                "message": "Server error."

            }

        ), 500
