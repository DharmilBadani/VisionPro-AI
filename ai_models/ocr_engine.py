try:
    import easyocr
except Exception:  # pragma: no cover - defensive fallback
    easyocr = None


class OCREngine:

    def __init__(self):

        if easyocr is None:
            self.reader = None
            return

        try:
            self.reader = easyocr.Reader(
                ["en"],
                gpu=False
            )
        except Exception:
            self.reader = None

    def extract_text(
        self,
        image_path
    ):

        if self.reader is None:
            return "OCR service unavailable."

        try:
            results = self.reader.readtext(
                image_path
            )
        except Exception:
            return "OCR service unavailable."

        extracted_text = []

        for result in results:

            extracted_text.append(
                result[1]
            )

        return "\n".join(
            extracted_text
        )