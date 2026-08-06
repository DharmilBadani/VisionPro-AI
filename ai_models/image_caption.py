class ImageCaptioner:
    """Generates natural language captions for uploaded images.
    
    Synthesizes predictions from the image classifier and detector
    into a coherent, descriptive visual caption.
    """

    @staticmethod
    def generate_caption(label, confidence, detections=None):
        if label and label.lower() == "pdf_document":
            return "An uploaded PDF document file parsed for text extraction."

        if not label or label.lower() in ("generic image", "unable to classify"):
            if detections:
                objects_str = ", ".join(set(d["label"] for d in detections))
                return f"An image containing the following detected elements: {objects_str}."
            return "A photograph containing visual elements that could not be confidently categorized."

        # Clean label for readability (convert underscores to spaces, capitalize)
        clean_label = label.replace("_", " ").title()

        if not detections:
            return f"A detailed view of a {clean_label}, identified with {confidence:.1f}% confidence."

        # Group and count detections
        counts = {}
        for d in detections:
            obj = d["label"].replace("_", " ").lower()
            counts[obj] = counts.get(obj, 0) + 1

        detected_list = []
        for obj, count in counts.items():
            if count > 1:
                detected_list.append(f"{count} {obj}s")
            else:
                # Add correct a/an prefix
                prefix = "an" if obj[0] in "aeiou" else "a"
                detected_list.append(f"{prefix} {obj}")

        if len(detected_list) == 1:
            details = f"accompanied by {detected_list[0]}"
        elif len(detected_list) > 1:
            details = f"with {', '.join(detected_list[:-1])} and {detected_list[-1]} visible in the scene"
        else:
            details = ""

        caption = f"A photograph of a {clean_label} (classified with {confidence:.1f}% confidence)"
        if details:
            caption += f", {details}."
        else:
            caption += "."

        return caption
