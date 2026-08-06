from flask import (
    Blueprint,
    render_template,
    send_file,
    abort
)

from flask_login import (
    login_required,
    current_user
)

from database.models import (
    Report
)

report_bp = Blueprint(
    "report",
    __name__
)


@report_bp.route("/reports")
@login_required
def reports():

    user_reports = (
        Report.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            Report.created_at.desc()
        )
        .all()
    )

    return render_template(
        "reports.html",
        reports=user_reports
    )


@report_bp.route("/preview-report/<int:report_id>")
@login_required
def preview_report(report_id):
    report = (
        Report.query
        .filter_by(
            id=report_id,
            user_id=current_user.id
        )
        .first()
    )

    if not report:
        abort(404)

    # Inline preview for iframe (no download)
    return send_file(
        report.report_path,
        as_attachment=False
    )


@report_bp.route("/download-report/<int:report_id>")
@login_required
def download_report(report_id):
    report = (
        Report.query
        .filter_by(
            id=report_id,
            user_id=current_user.id
        )
        .first()
    )

    if not report:
        abort(404)

    # Download only when user explicitly clicks Download
    return send_file(
        report.report_path,
        as_attachment=True
    )
