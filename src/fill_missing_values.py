import pandas as pd

df = pd.read_csv("worldbank_pca_policy_data_2010_2023.csv")

# Sort first
df = df.sort_values(["country", "year"])

# Fill missing secondary school enrollment country-wise
df["secondary_school_enrollment_gross_pct"] = (
    df.groupby("country")["secondary_school_enrollment_gross_pct"]
    .transform(lambda x: x.interpolate(method="linear").ffill().bfill())
)

print("Missing values after filling:")
print(df["secondary_school_enrollment_gross_pct"].isnull().sum())

df.to_csv("worldbank_pca_policy_data_cleaned.csv", index=False)

print("Cleaned file saved: worldbank_pca_policy_data_cleaned.csv")

print("After msiing in the values")
import pandas as pd

df = pd.read_csv("worldbank_pca_policy_data_cleaned.csv")

print("Missing values after cleaning:")
print(df.isnull().sum())