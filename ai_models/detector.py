from PIL import Image, ImageDraw, ImageFont

try:
    from ultralytics import YOLO
except Exception:  # pragma: no cover - defensive fallback
    YOLO = None


class ObjectDetector:

    def __init__(self):
        if YOLO is None:
            self.model = None
            return

        try:
            self.model = YOLO("yolov8n.pt")
        except Exception:
            self.model = None

    def detect(self, image_path, output_path=None):
        if self.model is None:
            return []

        try:
            results = self.model(image_path)
        except Exception:
            return []

        detected_objects = []

        # Annotate image if output_path is specified
        if output_path and results:
            try:
                img = Image.open(image_path).convert("RGB")
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.load_default()
                except Exception:
                    font = None

                for result in results:
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        confidence = float(box.conf[0])
                        label = self.model.names[class_id]
                        xyxy = box.xyxy[0].tolist()
                        xmin, ymin, xmax, ymax = xyxy

                        # Draw bounding box
                        draw.rectangle([xmin, ymin, xmax, ymax], outline="#7C3AED", width=3)

                        # Draw background label box
                        text = f"{label} {confidence*100:.0f}%"
                        # Approximate bounding box for font to support old and new pillow versions without deprecations
                        text_w = len(text) * 6
                        text_h = 10
                        draw.rectangle([xmin, ymin - text_h - 2, xmin + text_w + 4, ymin], fill="#7C3AED")
                        
                        if font:
                            draw.text((xmin + 2, ymin - text_h - 1), text, fill="#FFFFFF", font=font)
                        else:
                            draw.text((xmin, ymin - 10), text, fill="#7C3AED")
                
                img.save(output_path)
            except Exception as e:
                print(f"Failed to draw boxes: {e}")

        # Parse detected objects list
        for result in results:
            boxes = result.boxes
            for box in boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                label = self.model.names[class_id]

                detected_objects.append(
                    {
                        "label": label,
                        "confidence": round(confidence * 100, 2)
                    }
                )

        return detected_objects