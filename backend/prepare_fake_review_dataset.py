import pandas as pd


DATASET_PATH = "fake reviews dataset.csv"


df = pd.read_csv(DATASET_PATH)

print("\n========== DATASET INFORMATION ==========")

print("Total reviews:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nLabel distribution:")
print(df["label"].value_counts())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDataset shape:", df.shape)

print("=========================================")