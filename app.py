import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman

from config.settings import Config
from config.database import (
    init_database,
    login_manager
)

from utils.helpers import (
    ensure_directory,
    format_datetime
)

from utils.rate_limiter import init_limiter


csrf = CSRFProtect()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    csrf.init_app(app)

    Talisman(
        app,
        content_security_policy=None,
        force_https=False,
    )

    init_database(app)

    ensure_directory(app.config["UPLOAD_FOLDER"])
    ensure_directory(app.config["REPORT_FOLDER"])
    ensure_directory("logs")
    ensure_directory("instance")

    register_blueprints(app)
    register_filters(app)
    register_error_handlers(app)

    # Rate limiter (Flask-Limiter)
    init_limiter(app)

    return app



def register_blueprints(app):

    from routes.auth_routes import auth_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.image_routes import image_bp
    from routes.report_routes import report_bp
    from routes.api_routes import api_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)



def register_filters(app):

    @app.template_filter("datetime")
    def datetime_filter(value):
        return format_datetime(value)


def register_error_handlers(app):

    from flask import render_template

    @app.errorhandler(404)
    def not_found(error):
        return render_template(
            "error.html",
            title="404 Error",
            message="Page not found."
        ), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template(
            "error.html",
            title="500 Error",
            message="Internal server error."
        ), 500


@login_manager.unauthorized_handler
def unauthorized():
    from flask import redirect, url_for

    return redirect(
        url_for("auth.login")
    )


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )