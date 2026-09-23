import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

import joblib


DATASET_PATH = "fake reviews dataset.csv"


# 1. Load dataset
df = pd.read_csv(DATASET_PATH)

print("\n========== LOADING DATASET ==========")
print("Total reviews:", len(df))


# 2. Convert labels
df["label"] = df["label"].map({
    "CG": 1,
    "OR": 0
})


# 3. Review text
X_text = df["text_"].astype(str)
y = df["label"]


# 4. TF-IDF
print("\nCreating TF-IDF features...")

vectorizer = TfidfVectorizer(
    max_features=1500,
    stop_words="english"
)

X = vectorizer.fit_transform(X_text)


# 5. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n========== DATA SPLIT ==========")
print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])


# 6. Random Forest
print("\nTraining Random Forest...")

model = RandomForestClassifier(
    n_estimators=60,
    max_depth=16,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# 7. Prediction
y_pred = model.predict(X_test)


# 8. Evaluation
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)


print("\n========== MODEL RESULTS ==========")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Genuine", "Fake"]
    )
)

print("===================================")


# 9. Save model and vectorizer
joblib.dump(
    model,
    "backend/fake_review_random_forest.pkl"
)

joblib.dump(
    vectorizer,
    "backend/tfidf_vectorizer.pkl"
)

print("\n[OK] Model saved successfully!")
print("Model: backend/fake_review_random_forest.pkl")
print("Vectorizer: backend/tfidf_vectorizer.pkl")