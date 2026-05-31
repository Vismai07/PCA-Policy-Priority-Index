import pandas as pd

df = pd.read_csv("worldbank_pca_policy_data_2010_2023.csv")

print("Dataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns)

print("\nMissing values:")
print(df.isnull().sum())

print("\nFirst 10 rows:")
print(df.head(10))