import os
import uuid

from datetime import datetime

from werkzeug.utils import secure_filename


def ensure_directory(path):

    os.makedirs(
        path,
        exist_ok=True
    )


def secure_image_filename(filename):

    return secure_filename(
        filename
    )


def generate_unique_filename(filename):

    if not filename:
        return f"{uuid.uuid4().hex}.bin"

    if "." in filename:
        extension = filename.rsplit(
            ".",
            1
        )[1].strip().lower()
        if extension:
            return f"{uuid.uuid4().hex}.{extension}"

    return f"{uuid.uuid4().hex}.bin"


def format_datetime(value):

    if not value:
        return ""

    return value.strftime(
        "%d-%m-%Y %H:%M:%S"
    )