from ai_models.image_caption import ImageCaptioner
from ai_models.similarity_search import SimilaritySearcher


def test_image_captioner_basic():
    caption = ImageCaptioner.generate_caption("golden_retriever", 98.543)
    assert "Golden Retriever" in caption
    assert "98.5%" in caption
    assert "detailed view" in caption


def test_image_captioner_with_detections():
    detections = [{"label": "dog", "confidence": 99.1}]
    caption = ImageCaptioner.generate_caption("golden_retriever", 98.543, detections)
    assert "accompanied by a dog" in caption

    detections = [
        {"label": "dog", "confidence": 99.1},
        {"label": "dog", "confidence": 95.2},
        {"label": "frisbee", "confidence": 88.0}
    ]
    caption = ImageCaptioner.generate_caption("golden_retriever", 98.543, detections)
    assert "2 dogs and a frisbee" in caption or "2 dogs" in caption


def test_image_captioner_fallback():
    caption = ImageCaptioner.generate_caption("unable to classify", 0.0)
    assert "visual elements that could not be confidently categorized" in caption

    detections = [{"label": "cat", "confidence": 90.0}]
    caption = ImageCaptioner.generate_caption("generic image", 0.0, detections)
    assert "containing the following detected elements: cat" in caption or "cat" in caption


def test_similarity_searcher_empty():
    results = SimilaritySearcher.find_similar_images(1, "generic image")
    assert results == []

    results = SimilaritySearcher.find_similar_images(1, None)
    assert results == []


def test_image_classifier_selection(monkeypatch):
    from ai_models.classifier import ImageClassifier

    classifier = ImageClassifier()
    classifier._predict_fns["resnet50"] = lambda image_path, top_k: [{"label": "dummy_resnet", "confidence": 99.0}]
    classifier._predict_fns["mobilenet_v2"] = lambda image_path, top_k: [{"label": "dummy_mobilenet", "confidence": 95.0}]

    monkeypatch.setattr(classifier, "_load", lambda model_name: None)

    res = classifier.predict("fake.jpg", model_name="resnet50")
    assert res[0]["label"] == "dummy_resnet"

    res2 = classifier.predict("fake.jpg", model_name="mobilenet_v2")
    assert res2[0]["label"] == "dummy_mobilenet"


def test_pdf_processing():
    from app import create_app
    flask_app = create_app()
    with flask_app.app_context():
        from services.prediction_service import PredictionService

        # Check that PDF paths bypass CNN and YOLO, returning expected static classes
        cls_res = PredictionService.classify_image(1, "doc.pdf", "doc.pdf")
        assert cls_res["prediction"]["label"] == "pdf_document"
        assert cls_res["prediction"]["confidence"] == 100.0

        det_res = PredictionService.detect_objects(1, "doc.pdf")
        assert det_res == []
