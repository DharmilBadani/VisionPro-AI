from flask import current_app

from PIL import Image



def validate_image_file(file):

    if not file:

        raise ValueError("No file provided.")

    if file.filename == "":

        raise ValueError("No file selected.")

    if "." not in file.filename:

        raise ValueError("Invalid file format.")

    extension = file.filename.rsplit(".", 1)[1].lower()

    if extension not in current_app.config["ALLOWED_EXTENSIONS"]:

        raise ValueError("Unsupported file format.")

    # Validate actual image integrity (prevents renamed non-images) for non-PDFs
    if extension != "pdf":
        stream = file.stream

        try:
            img = Image.open(stream)
            img.verify()
        except Exception:
            raise ValueError("Invalid or corrupted image file.")
        finally:
            try:
                stream.seek(0)
            except Exception:
                pass

    return True
