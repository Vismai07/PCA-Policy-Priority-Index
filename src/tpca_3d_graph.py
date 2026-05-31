import pandas as pd
import matplotlib.pyplot as plt

# 3D plotting tool from matplotlib
from mpl_toolkits.mplot3d import Axes3D

# --------------------------------------------------
# 1. Load PCA output files
# --------------------------------------------------
ranking = pd.read_csv("manual_pca_country_ranking_2022.csv")
loadings = pd.read_csv("manual_pca_loadings_2022.csv", index_col=0)

# --------------------------------------------------
# 2. 3D PCA country map
# --------------------------------------------------
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection="3d")

ax.scatter(
    ranking["PC1_score"],
    ranking["PC2_score"],
    ranking["PC3_score"],
    s=80
)

# Add country labels
for _, row in ranking.iterrows():
    ax.text(
        row["PC1_score"],
        row["PC2_score"],
        row["PC3_score"],
        row["country"],
        fontsize=8
    )

ax.set_xlabel("PC1: Development Capacity")
ax.set_ylabel("PC2: Secondary Policy Dimension")
ax.set_zlabel("PC3: Structural Development Dimension")

ax.set_title("3D PCA Country Map: Emerging Economies, 2022")

plt.tight_layout()
plt.savefig("pca_3d_country_map_2022.png", dpi=300)
plt.show()

# --------------------------------------------------
# 3. 3D PCA biplot with indicator arrows
# --------------------------------------------------
fig = plt.figure(figsize=(13, 10))
ax = fig.add_subplot(111, projection="3d")

# Plot country points
ax.scatter(
    ranking["PC1_score"],
    ranking["PC2_score"],
    ranking["PC3_score"],
    s=80
)

# Add country labels
for _, row in ranking.iterrows():
    ax.text(
        row["PC1_score"],
        row["PC2_score"],
        row["PC3_score"],
        row["country"],
        fontsize=8
    )

# Indicator arrows
arrow_scale = 4

for indicator in loadings.index:
    pc1 = loadings.loc[indicator, "PC1"]
    pc2 = loadings.loc[indicator, "PC2"]
    pc3 = loadings.loc[indicator, "PC3"]

    ax.quiver(
        0, 0, 0,
        pc1 * arrow_scale,
        pc2 * arrow_scale,
        pc3 * arrow_scale,
        arrow_length_ratio=0.1
    )

    ax.text(
        pc1 * arrow_scale * 1.15,
        pc2 * arrow_scale * 1.15,
        pc3 * arrow_scale * 1.15,
        indicator,
        fontsize=7
    )

ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_zlabel("PC3")

ax.set_title("3D PCA Biplot: Countries and Development Indicators")

plt.tight_layout()
plt.savefig("pca_3d_biplot_2022.png", dpi=300)
plt.show()

print("3D PCA graphs created:")
print("pca_3d_country_map_2022.png")
print("pca_3d_biplot_2022.png")