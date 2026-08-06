import warnings

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def init_limiter(app):
    """Initialize Flask-Limiter.

    Tests run with `-W error` in some environments; suppress limiter UserWarnings
    about default in-memory storage.
    """

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            message=r"Using the in-memory storage for tracking rate limits.*",
            category=UserWarning,
        )
        limiter = Limiter(
            key_func=get_remote_address,
            app=app,
            default_limits=["30 per minute"],
        )

    return limiter


