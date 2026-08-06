import os

from flask import current_app

from utils.validators import (
    validate_image_file
)

from utils.helpers import (
    generate_unique_filename,
    secure_image_filename
)


class ImageService:

    @staticmethod
    def save_uploaded_image(file):

        validate_image_file(file)

        original_filename = secure_image_filename(
            file.filename
        )

        filename = generate_unique_filename(
            original_filename
        )

        upload_folder = current_app.config[
            "UPLOAD_FOLDER"
        ]

        os.makedirs(
            upload_folder,
            exist_ok=True
        )

        file_path = os.path.join(
            upload_folder,
            filename
        )

        file.save(file_path)

        return {
            "filename": filename,
            "file_path": file_path
        }