import pandas as pd
import numpy as np

# --------------------------------------------------
# 1. Load PCA-ready data
# --------------------------------------------------
df = pd.read_csv("pca_ready_2022.csv")

# --------------------------------------------------
# 2. Select PCA indicator columns
# --------------------------------------------------
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

# Data matrix X
X = df[pca_columns].values

# --------------------------------------------------
# 3. Manual standardization
# Formula: Z = (X - mean) / standard deviation
# --------------------------------------------------
mean_values = np.mean(X, axis=0)
std_values = np.std(X, axis=0, ddof=1)

Z = (X - mean_values) / std_values

standardized_df = pd.DataFrame(Z, columns=pca_columns)
standardized_df.insert(0, "country", df["country"])

print("\nStandardized data:")
print(standardized_df)

# --------------------------------------------------
# 4. Manual covariance matrix
# Formula: C = (Z.T @ Z) / (n - 1)
# --------------------------------------------------
n = Z.shape[0]
cov_matrix = (Z.T @ Z) / (n - 1)

cov_df = pd.DataFrame(cov_matrix, index=pca_columns, columns=pca_columns)

print("\nCovariance matrix:")
print(cov_df)

# --------------------------------------------------
# 5. Eigen decomposition
# Formula: C v = lambda v
# --------------------------------------------------
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

# Convert tiny complex values to real
eigenvalues = eigenvalues.real
eigenvectors = eigenvectors.real

# --------------------------------------------------
# 6. Sort eigenvalues and eigenvectors descending
# --------------------------------------------------
sorted_indices = np.argsort(eigenvalues)[::-1]

eigenvalues_sorted = eigenvalues[sorted_indices]
eigenvectors_sorted = eigenvectors[:, sorted_indices]

# --------------------------------------------------
# 7. Explained variance
# --------------------------------------------------
explained_variance_ratio = eigenvalues_sorted / np.sum(eigenvalues_sorted)
cumulative_variance = np.cumsum(explained_variance_ratio)

explained_variance_df = pd.DataFrame({
    "principal_component": [f"PC{i+1}" for i in range(len(pca_columns))],
    "eigenvalue": eigenvalues_sorted,
    "explained_variance_ratio": explained_variance_ratio,
    "cumulative_variance": cumulative_variance
})

print("\nExplained variance:")
print(explained_variance_df)

# --------------------------------------------------
# 8. PCA loadings
# Each column shows contribution of indicators to PC
# --------------------------------------------------
loadings = pd.DataFrame(
    eigenvectors_sorted,
    index=pca_columns,
    columns=[f"PC{i+1}" for i in range(len(pca_columns))]
)

print("\nPCA loadings:")
print(loadings)

# --------------------------------------------------
# 9. PCA scores
# Formula: Scores = Z @ eigenvectors
# --------------------------------------------------
scores = Z @ eigenvectors_sorted

df["PC1_score"] = scores[:, 0]
df["PC2_score"] = scores[:, 1]
df["PC3_score"] = scores[:, 2]

# --------------------------------------------------
# 10. Fix PC1 direction
# If GDP loading is negative, reverse PC1
# PCA sign can flip naturally, so this is acceptable.
# --------------------------------------------------
if loadings.loc["gdp_per_capita_constant_2015_usd", "PC1"] < 0:
    df["PC1_score"] = -1 * df["PC1_score"]
    loadings["PC1"] = -1 * loadings["PC1"]

# --------------------------------------------------
# 11. Rank countries
# --------------------------------------------------
ranking = df.sort_values("PC1_score", ascending=False).copy()

# --------------------------------------------------
# 12. Add policy category
# --------------------------------------------------
def policy_category(score):
    if score >= 1:
        return "Strong development position"
    elif score >= -1:
        return "Moderate / transitional"
    else:
        return "High policy priority"

ranking["policy_category"] = ranking["PC1_score"].apply(policy_category)

print("\nCountry ranking:")
print(ranking[["country", "PC1_score", "PC2_score", "PC3_score", "policy_category"]])
# --------------------------------------------------
# 13. Save output files
# --------------------------------------------------
standardized_df.to_csv("manual_pca_standardized_data_2022.csv", index=False)
cov_df.to_csv("manual_pca_covariance_matrix_2022.csv")
explained_variance_df.to_csv("manual_pca_explained_variance_2022.csv", index=False)
loadings.to_csv("manual_pca_loadings_2022.csv")
ranking.to_csv("manual_pca_country_ranking_2022.csv", index=False)

print("\nSaved files:")
print("manual_pca_standardized_data_2022.csv")
print("manual_pca_covariance_matrix_2022.csv")
print("manual_pca_explained_variance_2022.csv")
print("manual_pca_loadings_2022.csv")
print("manual_pca_country_ranking_2022.csv")