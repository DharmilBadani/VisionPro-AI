from flask import (
    Blueprint,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from services.analytics_service import (
    AnalyticsService
)
from services.prediction_service import PredictionService

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def home():

    return render_template(
        "index.html"
    )


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    stats = (
        AnalyticsService.get_dashboard_stats(
            current_user.id
        )
    )

    chart_data = (
        AnalyticsService.get_top_predictions(
            current_user.id
        )
    )

    return render_template(
        "dashboard.html",
        stats=stats,
        chart_data=chart_data
    )


@dashboard_bp.route("/history")
@login_required
def history():

    prediction_type = request.args.get("prediction_type", "")
    min_confidence = request.args.get("min_confidence", "")
    search_text = request.args.get("search_text", "")

    history_data = (
        AnalyticsService.get_prediction_history(
            current_user.id,
            prediction_type=prediction_type or None,
            min_confidence=min_confidence or None,
            search_text=search_text or None,
        )
    )

    return render_template(
        "history.html",
        history=history_data,
        filters={
            "prediction_type": prediction_type,
            "min_confidence": min_confidence,
            "search_text": search_text,
        },
    )


@dashboard_bp.route("/history/export")
@login_required
def export_history():
    history_data = AnalyticsService.get_prediction_history(current_user.id)
    rows = ["id,prediction,confidence,created_at\n"]
    for item in history_data:
        rows.append(f"{item.id},{item.prediction},{item.confidence},{item.created_at}\n")
    csv_content = "".join(rows)
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=history.csv"},
    )


import time

@dashboard_bp.route("/compare-models", methods=["GET", "POST"])
@login_required
def compare_models():
    if request.method == "POST":
        image_file = request.files.get("image")
        if not image_file:
            flash("Please select an image.", "danger")
            return redirect(url_for("dashboard.compare_models"))

        from services.image_service import ImageService

        image_info = ImageService.save_uploaded_image(image_file)

        # Run ResNet50
        start_resnet = time.time()
        resnet_classification = PredictionService.classify_image(
            current_user.id,
            image_info["filename"],
            image_info["file_path"],
            model_name="resnet50"
        )
        resnet_duration = round((time.time() - start_resnet) * 1000, 1)

        # Run MobileNetV2
        start_mobilenet = time.time()
        mobilenet_classification = PredictionService.classify_image(
            current_user.id,
            image_info["filename"],
            image_info["file_path"],
            model_name="mobilenet_v2"
        )
        mobilenet_duration = round((time.time() - start_mobilenet) * 1000, 1)

        return render_template(
            "compare_models.html",
            image_filename=image_info["filename"],
            resnet_prediction=resnet_classification["prediction"],
            resnet_predictions=resnet_classification["top_predictions"],
            resnet_duration=resnet_duration,
            mobilenet_prediction=mobilenet_classification["prediction"],
            mobilenet_predictions=mobilenet_classification["top_predictions"],
            mobilenet_duration=mobilenet_duration
        )

    return render_template("compare_models.html")