from database.models import Prediction


class SimilaritySearcher:
    """Finds visually or semantically similar images in the user's upload history."""

    @staticmethod
    def find_similar_images(user_id, current_label, current_image_path=None, limit=3):
        if not current_label or current_label.lower() in ("generic image", "unable to classify"):
            return []

        # Query database for predictions with matching labels for this user
        query = Prediction.query.filter(
            Prediction.user_id == user_id,
            Prediction.prediction == current_label
        )
        
        if current_image_path:
            query = query.filter(Prediction.image_path != current_image_path)

        results = query.order_by(Prediction.created_at.desc()).limit(limit).all()

        similar_items = []
        for r in results:
            similar_items.append({
                "id": r.id,
                "image_name": r.image_name,
                "prediction": r.prediction,
                "confidence": r.confidence,
                "created_at": r.created_at
            })

        return similar_items
