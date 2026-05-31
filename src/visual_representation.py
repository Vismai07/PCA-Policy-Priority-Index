import pandas as pd
import matplotlib.pyplot as plt

ranking = pd.read_csv("manual_pca_country_ranking_2022.csv")
variance = pd.read_csv("manual_pca_explained_variance_2022.csv")
loadings = pd.read_csv("manual_pca_loadings_2022.csv", index_col=0)

# --------------------------------------------------
# 1. Country ranking bar chart
# --------------------------------------------------
ranking_sorted = ranking.sort_values("PC1_score")

plt.figure(figsize=(10, 6))
plt.barh(ranking_sorted["country"], ranking_sorted["PC1_score"])
plt.xlabel("PC1 Development Score")
plt.ylabel("Country")
plt.title("PCA-Based Development Score by Country, 2022")
plt.tight_layout()
plt.savefig("chart_country_pca_ranking_2022.png", dpi=300)
plt.close()

# --------------------------------------------------
# 2. Explained variance scree plot
# --------------------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(variance["principal_component"], variance["explained_variance_ratio"], marker="o")
plt.xlabel("Principal Component")
plt.ylabel("Explained Variance Ratio")
plt.title("Scree Plot: Explained Variance by Principal Component")
plt.tight_layout()
plt.savefig("chart_explained_variance_2022.png", dpi=300)
plt.close()

# --------------------------------------------------
# 3. PC1 vs PC2 scatter plot
# --------------------------------------------------
plt.figure(figsize=(8, 6))
plt.scatter(ranking["PC1_score"], ranking["PC2_score"])

for i, row in ranking.iterrows():
    plt.text(row["PC1_score"], row["PC2_score"], row["country"], fontsize=8)

plt.xlabel("PC1 Development Score")
plt.ylabel("PC2 Secondary Dimension")
plt.title("Country Positioning Using Manual PCA, 2022")
plt.tight_layout()
plt.savefig("chart_pc1_pc2_scatter_2022.png", dpi=300)
plt.close()

print("Charts saved successfully.")
