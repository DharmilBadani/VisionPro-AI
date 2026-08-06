import numpy as np


class ImageClassifier:
    """Lazy-loading classifier supporting multiple models.

    TensorFlow/Keras models are built only when predict() is called for that model.
    This keeps app/test imports fast and avoids crashes in CI.
    """

    def __init__(self):
        self._models = {}
        self._predict_fns = {}

    def _load(self, model_name: str):
        if model_name in self._models:
            return

        from tensorflow.keras.preprocessing import image  # type: ignore

        if model_name == "mobilenet_v2":
            from tensorflow.keras.applications.mobilenet_v2 import (  # type: ignore
                MobileNetV2,
                preprocess_input,
                decode_predictions,
            )
            model = MobileNetV2(weights="imagenet")
        else:
            # Default to higher accuracy ResNet50
            from tensorflow.keras.applications.resnet50 import (  # type: ignore
                ResNet50,
                preprocess_input,
                decode_predictions,
            )
            model = ResNet50(weights="imagenet")

        self._models[model_name] = model

        def predict_impl(image_path: str, top_k: int = 5):
            img = image.load_img(image_path, target_size=(224, 224))
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            predictions = model.predict(img_array, verbose=0)
            decoded = decode_predictions(predictions, top=top_k)[0]

            results = []
            for _, label, confidence in decoded:
                results.append(
                    {
                        "label": label,
                        "confidence": round(float(confidence) * 100, 2),
                    }
                )
            return results

        self._predict_fns[model_name] = predict_impl

    def predict(self, image_path: str, model_name: str = "mobilenet_v2", top_k: int = 5):
        try:
            self._load(model_name)
            return self._predict_fns[model_name](image_path, top_k=top_k)
        except Exception:
            return [
                {
                    "label": "Generic Image",
                    "confidence": 0.0,
                },
                {
                    "label": "Unable to classify",
                    "confidence": 0.0,
                },
            ]
