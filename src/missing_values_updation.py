import pandas as pd

df = pd.read_csv("worldbank_pca_policy_data_2010_2023.csv")

missing_secondary = df[df["secondary_school_enrollment_gross_pct"].isnull()]
print("Missing values for which country")
print(missing_secondary[["country", "year", "secondary_school_enrollment_gross_pct"]])
print("Total missing:", missing_secondary.shape[0])