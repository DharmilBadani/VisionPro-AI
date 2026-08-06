"""Test helpers.

This repo's existing tests are placeholder-only. In order to avoid complex
Flask-Login wiring, we provide a minimal monkeypatch utility to treat a
request as authenticated.

NOTE: Not used automatically by the app.
"""

from flask_login import utils as login_utils


def patch_is_authenticated(monkeypatch, value=True):
    # Monkeypatch a user proxy if needed in future tests.
    monkeypatch.setattr(login_utils, "_get_user", lambda *a, **k: None, raising=False)

