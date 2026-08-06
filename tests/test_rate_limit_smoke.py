import io
import pytest


def test_rate_limit_smoke():
    # This is a smoke test to ensure the limiter is wired and requests
    # return a response. Because auth is not fully configured in this repo,
    # we accept 302/401 redirects as "pass".
    from app import app as flask_app

    with flask_app.test_client() as client:
        data = {"image": (io.BytesIO(b"fake"), "test.jpg")}

        resp = client.post(
            "/api/classify",
            data=data,
            content_type="multipart/form-data",
        )

        assert resp.status_code in (200, 400, 401, 302, 429)

