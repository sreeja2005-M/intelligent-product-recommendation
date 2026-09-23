from datetime import datetime

import joblib

from backend.database import SessionLocal
from backend.models import Review, FakeReviewDetection


MODEL_PATH = "backend/fake_review_random_forest.pkl"
VECTORIZER_PATH = "backend/tfidf_vectorizer.pkl"


# Load trained model and TF-IDF vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def save_fake_predictions():

    db = SessionLocal()

    try:

        reviews = db.query(Review).all()

        print("\n========== FAKE REVIEW DETECTION ==========")
        print("Reviews found:", len(reviews))

        saved_count = 0

        for review in reviews:

            review_text = review.review_text or ""

            # Convert review text into TF-IDF features
            review_vector = vectorizer.transform(
                [review_text]
            )

            # Predict
            prediction = model.predict(review_vector)[0]

            probabilities = model.predict_proba(
                review_vector
            )[0]

            genuine_probability = probabilities[0]
            fake_probability = probabilities[1]

            is_fake = int(prediction)

            if is_fake == 1:
                reason = (
                    "ML model classified the review as "
                    "potentially fake"
                )
            else:
                reason = (
                    "ML model classified the review as "
                    "likely genuine"
                )

            result = FakeReviewDetection(
                review_id=review.review_id,
                is_fake=is_fake,
                fake_score=fake_probability,
                reason=reason,
                analyzed_at=datetime.now()
            )

            db.add(result)

            saved_count += 1

            print(f"\nReview ID: {review.review_id}")
            print("Review:", review_text)
            print(
                "Prediction:",
                "Fake" if is_fake else "Genuine"
            )
            print(
                f"Fake Probability: "
                f"{fake_probability:.4f}"
            )

        db.commit()

        print("\n============================================")
        print("Fake review records saved:", saved_count)
        print("============================================")

    except Exception as e:

        db.rollback()

        print("\n❌ Fake review save failed!")
        print("Error:", e)

    finally:

        db.close()


if __name__ == "__main__":
    save_fake_predictions()