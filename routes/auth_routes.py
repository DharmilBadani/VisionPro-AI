from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from forms.auth_forms import (
    LoginForm,
    RegisterForm
)

from services.auth_service import AuthService

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if current_user.is_authenticated:
        return redirect(
            url_for("auth.profile")
        )

    form = RegisterForm()

    if form.validate_on_submit():

        success, message = (
            AuthService.register_user(
                username=form.username.data.strip(),
                email=form.email.data.strip(),
                password=form.password.data
            )
        )

        if success:

            flash(
                message,
                "success"
            )

            return redirect(
                url_for("auth.login")
            )

        flash(
            message,
            "danger"
        )

    return render_template(
        "register.html",
        form=form
    )


@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:
        return redirect(
            url_for("auth.profile")
        )

    form = LoginForm()

    if request.method == "GET":
        remembered_email = request.cookies.get("remembered_email")
        if remembered_email:
            form.email.data = remembered_email
            form.remember_me.data = True

    if form.validate_on_submit():

        user = (
            AuthService.authenticate_user(
                form.email.data.strip(),
                form.password.data
            )
        )

        if not user:

            flash(
                "Invalid email or password.",
                "danger"
            )

            return render_template(
                "login.html",
                form=form
            )

        # Force session-based auth only.
        # This ensures closing the browser/window logs the user out by default.
        login_user(
            user,
            remember=False
        )

        flash(
            "Login successful.",
            "success"
        )

        next_page = request.args.get("next")
        response = redirect(next_page if next_page else url_for("auth.profile"))

        if form.remember_me.data:
            # Save email in cookie for 30 days
            response.set_cookie(
                "remembered_email",
                form.email.data.strip(),
                max_age=30 * 24 * 60 * 60,
                httponly=True,
                samesite="Lax"
            )
        else:
            response.delete_cookie("remembered_email")

        return response

    return render_template(
        "login.html",
        form=form
    )


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "info"
    )

    return redirect(
        url_for("auth.login")
    )


@auth_bp.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html"
    )