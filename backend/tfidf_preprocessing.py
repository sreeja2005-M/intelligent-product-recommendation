import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


DATASET_PATH = "fake reviews dataset.csv"


df = pd.read_csv(DATASET_PATH)

# Convert labels
df["label"] = df["label"].map({
    "CG": 1,
    "OR": 0
})

# Review text
X_text = df["text_"].astype(str)

# TF-IDF
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

X = vectorizer.fit_transform(X_text)

y = df["label"]

print("\n========== TF-IDF RESULT ==========")
print("Original reviews:", len(df))
print("TF-IDF shape:", X.shape)
print("Target shape:", y.shape)
print("Fake reviews (CG):", sum(y == 1))
print("Genuine reviews (OR):", sum(y == 0))
print("===================================")