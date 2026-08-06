from pathlib import Path


def test_base_template_uses_dark_theme():
    template = Path("templates/base.html").read_text(encoding="utf-8")

    assert 'data-bs-theme="dark"' in template
    assert 'data-theme="dark"' in template


def test_theme_script_forces_dark_theme():
    theme_js = Path("static/js/theme.js").read_text(encoding="utf-8")

    assert "data-theme = 'dark'" in theme_js or "dataset.theme = 'dark'" in theme_js or "data-theme='dark'" in theme_js
