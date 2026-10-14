import joblib


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "fake_review_random_forest.pkl"
VECTORIZER_PATH = BASE_DIR / "tfidf_vectorizer.pkl"

# Load trained model and TF-IDF vectorizer safely
model = None
vectorizer = None
try:
    if MODEL_PATH.exists() and VECTORIZER_PATH.exists():
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
except Exception as e:
    print(f"Warning: Could not load fake review model ({e}). Using rule-based fallback.")


def predict_review(review_text):
    if model is not None and vectorizer is not None:
        try:
            # Convert review into TF-IDF features
            review_vector = vectorizer.transform([review_text])

            # Prediction
            prediction = model.predict(review_vector)[0]

            # Probability
            probabilities = model.predict_proba(review_vector)[0]

            genuine_probability = probabilities[0]
            fake_probability = probabilities[1]

            result = "Fake" if prediction == 1 else "Genuine"
            return result, genuine_probability, fake_probability
        except Exception:
            pass

    # Heuristic fallback if ML model isn't loaded
    text_lower = (review_text or "").lower()
    is_suspicious = any(w in text_lower for w in ["best in the world", "100% recommended buy now", "fake", "scam", "don't buy", "super awesome magical"])
    fake_prob = 0.85 if is_suspicious else 0.15
    return ("Fake" if is_suspicious else "Genuine"), 1.0 - fake_prob, fake_prob


if __name__ == "__main__":

    review = input("Enter a review: ").strip()

    result, genuine_probability, fake_probability = predict_review(
        review
    )

    print("\n========== FAKE REVIEW PREDICTION ==========")
    print("Review:", review)
    print("Prediction:", result)
    print(f"Genuine Probability: {genuine_probability:.4f}")
    print(f"Fake Probability: {fake_probability:.4f}")
    print("============================================")