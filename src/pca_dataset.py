import pandas as pd

# Load cleaned data
df = pd.read_csv("worldbank_pca_policy_data_cleaned.csv")

# Select year
df_2022 = df[df["year"] == 2022].copy()

# PCA columns
pca_columns = [
    "gdp_per_capita_constant_2015_usd",
    "gdp_growth_annual_pct",
    "adjusted_inflation_annual_pct",
    "adjusted_unemployment_total_pct_ilo_estimate",
    "life_expectancy_years",
    "adjusted_infant_mortality_per_1000_live_births",
    "secondary_school_enrollment_gross_pct",
    "access_to_electricity_pct_population",
    "individuals_using_internet_pct_population",
    "trade_pct_gdp"
]

# Keep only country info + PCA columns
pca_df = df_2022[["country_code", "country", "year"] + pca_columns].copy()

print("Before dropping missing values:")
print(pca_df.isnull().sum())

# Remove rows with missing values
pca_df = pca_df.dropna()

print("\nAfter dropping missing values:")
print(pca_df.isnull().sum())

print("\nPCA-ready shape:")
print(pca_df.shape)

print("\nPCA-ready data:")
print(pca_df)

# Save PCA-ready data
pca_df.to_csv("pca_ready_2022.csv", index=False)

print("\nSaved: pca_ready_2022.csv")