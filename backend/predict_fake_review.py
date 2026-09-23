import joblib


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "fake_review_random_forest.pkl"
VECTORIZER_PATH = BASE_DIR / "tfidf_vectorizer.pkl"

# Load trained model and TF-IDF vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def predict_review(review_text):

    # Convert review into TF-IDF features
    review_vector = vectorizer.transform([review_text])

    # Prediction
    prediction = model.predict(review_vector)[0]

    # Probability
    probabilities = model.predict_proba(review_vector)[0]

    genuine_probability = probabilities[0]
    fake_probability = probabilities[1]

    if prediction == 1:
        result = "Fake"
    else:
        result = "Genuine"

    return result, genuine_probability, fake_probability


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