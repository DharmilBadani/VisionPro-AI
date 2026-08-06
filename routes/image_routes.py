from flask import (
    Blueprint,
    render_template,
    request,
    flash
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

from services.report_service import (
    ReportService
)

image_bp = Blueprint(
    "image",
    __name__
)


@image_bp.route(
    "/upload",
    methods=["GET", "POST"]
)
@login_required
def upload():

    if request.method == "POST":

        image_file = request.files.get(
            "image"
        )

        if not image_file:

            flash(
                "Please select an image.",
                "danger"
            )

            return render_template(
                "prediction.html"
            )

        try:

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

            import os
            predictions_folder = os.path.join("static", "predictions")
            os.makedirs(predictions_folder, exist_ok=True)
            
            is_pdf = image_info["filename"].lower().endswith(".pdf")
            annotated_filename = None if is_pdf else f"annotated_{image_info['filename']}"
            annotated_filepath = None if is_pdf else os.path.join(predictions_folder, annotated_filename)

            detections = (
                PredictionService.detect_objects(
                    current_user.id,
                    image_info["file_path"],
                    output_path=annotated_filepath
                )
            )

            extracted_text = (
                PredictionService.extract_text(
                    current_user.id,
                    image_info["file_path"]
                )
            )

            report = (
                ReportService.generate_report(
                    current_user.id,
                    classification["prediction"]["label"],
                    classification["prediction"]["confidence"],
                    extracted_text
                )
            )

            caption = PredictionService.generate_and_save_caption(
                current_user.id,
                image_info["file_path"],
                classification["prediction"]["label"],
                classification["prediction"]["confidence"],
                detections
            )

            from ai_models.similarity_search import SimilaritySearcher
            similar_images = SimilaritySearcher.find_similar_images(
                current_user.id,
                classification["prediction"]["label"],
                current_image_path=image_info["file_path"]
            )

            return render_template(
                "prediction.html",
                image_filename=image_info["filename"],
                annotated_filename=annotated_filename,
                prediction=classification["prediction"],
                predictions=classification["top_predictions"],
                detections=detections,
                extracted_text=extracted_text,
                report_id=report.id,
                generated_caption=caption,
                similar_images=similar_images
            )

        except Exception as exc:

            flash(
                str(exc),
                "danger"
            )

    return render_template(
        "prediction.html"
    )