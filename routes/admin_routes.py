from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from forms.auth_forms import LoginForm

from services.auth_service import AuthService
from services.analytics_service import AnalyticsService

from config.database import db
from database.models import User, Report, Prediction, ActivityLog

from werkzeug.security import check_password_hash


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


def _is_admin(user: User) -> bool:

    return (
        user is not None and
        getattr(user, "role", None) == "admin" and
        getattr(user, "is_active", True)
    )





@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        if _is_admin(current_user):
            return redirect(url_for("admin.users"))
        return redirect(url_for("auth.profile"))

    form = LoginForm()

    # Hardcoded admin credentials (no self-registration)
    # Username = Admin123
    # Password = admin@1234
    HARDCODED_ADMIN_USERNAME = "Admin123"
    HARDCODED_ADMIN_PASSWORD = "admin@1234"

    # Handle POST explicitly and only require the password to match.
    # The LoginForm always has email+password validators; however, your UI flow
    # may be submitting only the password field (email empty), which causes validation fail.
    # So we validate password manually after a successful POST.
    if request.method == "POST":

        admin_username_or_email = form.email.data.strip() if form.email.data else ""
        password = form.password.data


        # (Safety) Ensure we only ever authenticate the single hardcoded admin.
        # This keeps redirect target consistent: /admin/users


        if admin_username_or_email != HARDCODED_ADMIN_USERNAME:
            flash("Invalid admin email or password.", "danger")
            return render_template("admin_login.html", form=form)

        if password != HARDCODED_ADMIN_PASSWORD:
            flash("Invalid admin email or password.", "danger")
            return render_template("admin_login.html", form=form)

        # Create or update the admin DB user row.
        from werkzeug.security import generate_password_hash

        # Store admin user by email field, but admin login form provides username.
        # Use a dedicated deterministic email for admin row.
        ADMIN_EMAIL_FOR_DB = "admin@visionai-pro.local"

        admin_user = User.query.filter_by(email=ADMIN_EMAIL_FOR_DB).first()

        if not admin_user:
            admin_user = User(
                username=HARDCODED_ADMIN_USERNAME,
                email=ADMIN_EMAIL_FOR_DB,
                password_hash=generate_password_hash(password),
                role="admin"
            )
            db.session.add(admin_user)
            db.session.commit()
        else:
            admin_user.role = "admin"
            admin_user.password_hash = generate_password_hash(password)
            db.session.commit()


        if not _is_admin(admin_user):
            # Even if credentials are correct, enforce role.
            flash("Admin account is not active/authorized.", "danger")
            return render_template("admin_login.html", form=form)

        login_user(admin_user, remember=False)
        flash("Admin login successful.", "success")
        return redirect(url_for("admin.users"))

    return render_template("admin_login.html", form=form)


@admin_bp.route("/logout", methods=["POST", "GET"])
@login_required
def logout():

    if not _is_admin(current_user):
        abort(403)

    logout_user()
    # Signal the UI to show signing-off animation
    return redirect(url_for("admin.signoff"))


@admin_bp.route("/signoff")
def signoff():

    # No login required: after logout.
    return render_template("admin_signoff.html")


@admin_bp.route("/users")
@login_required
def users():

    if not _is_admin(current_user):
        abort(403)

    all_users = User.query.order_by(User.created_at.desc()).all()

    # Precompute small stats set for list page.
    user_rows = []
    for u in all_users:
        stats = AnalyticsService.get_dashboard_stats(u.id)
        user_rows.append((u, stats))

    return render_template("admin_users.html", users=user_rows)


@admin_bp.route("/users/<int:user_id>")
@login_required
def user_details(user_id: int):

    if not _is_admin(current_user):
        abort(403)

    user = User.query.get_or_404(user_id)

    stats = AnalyticsService.get_dashboard_stats(user.id)

    user_reports = (
        Report.query
        .filter_by(user_id=user.id)
        .order_by(Report.created_at.desc())
        .all()
    )

    user_top_predictions = AnalyticsService.get_top_predictions(user.id)

    # Also show recent prediction records for a richer “usage” view.
    recent_usage = (
        Prediction.query
        .filter_by(user_id=user.id)
        .order_by(Prediction.created_at.desc())
        .limit(10)
        .all()
    )

    activity_feed = (
        ActivityLog.query
        .filter_by(user_id=user.id)
        .order_by(ActivityLog.created_at.desc())
        .limit(20)
        .all()
    )

    return render_template(
        "admin_user_details.html",
        user=user,
        stats=stats,
        reports=user_reports,
        top_predictions=user_top_predictions,
        recent_usage=recent_usage,
        activity_feed=activity_feed
    )

