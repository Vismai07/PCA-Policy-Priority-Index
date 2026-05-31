import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Load manual PCA outputs
# --------------------------------------------------
ranking = pd.read_csv("manual_pca_country_ranking_2022.csv")
variance = pd.read_csv("manual_pca_explained_variance_2022.csv")
loadings = pd.read_csv("manual_pca_loadings_2022.csv", index_col=0)

# --------------------------------------------------
# 2. Scree plot
# --------------------------------------------------
plt.figure(figsize=(9, 5))

plt.plot(
    variance["principal_component"],
    variance["explained_variance_ratio"],
    marker="o"
)

plt.xlabel("Principal Components")
plt.ylabel("Explained Variance Ratio")
plt.title("Scree Plot: Explained Variance by Principal Component")
plt.grid(True)
plt.tight_layout()
plt.savefig("advanced_scree_plot.png", dpi=300)
plt.show()

# --------------------------------------------------
# 3. PC1 vs PC2 country scatter plot
# --------------------------------------------------
plt.figure(figsize=(10, 7))

plt.scatter(
    ranking["PC1_score"],
    ranking["PC2_score"],
    s=80
)

for i, row in ranking.iterrows():
    plt.text(
        row["PC1_score"] + 0.03,
        row["PC2_score"] + 0.03,
        row["country"],
        fontsize=9
    )

plt.axhline(0, linewidth=1)
plt.axvline(0, linewidth=1)

plt.xlabel("PC1: Development / Policy Capacity Score")
plt.ylabel("PC2: Secondary Policy Dimension")
plt.title("PCA Country Map: PC1 vs PC2")
plt.grid(True)
plt.tight_layout()
plt.savefig("advanced_pc1_pc2_country_scatter.png", dpi=300)
plt.show()

# --------------------------------------------------
# 4. PCA Biplot with loading arrows
# --------------------------------------------------
plt.figure(figsize=(12, 8))

# Country points
plt.scatter(
    ranking["PC1_score"],
    ranking["PC2_score"],
    s=80
)

for i, row in ranking.iterrows():
    plt.text(
        row["PC1_score"] + 0.03,
        row["PC2_score"] + 0.03,
        row["country"],
        fontsize=9
    )

# Scale arrows so they are visible
arrow_scale = 4

for indicator in loadings.index:
    pc1_loading = loadings.loc[indicator, "PC1"]
    pc2_loading = loadings.loc[indicator, "PC2"]

    plt.arrow(
        0,
        0,
        pc1_loading * arrow_scale,
        pc2_loading * arrow_scale,
        head_width=0.06,
        length_includes_head=True
    )

    plt.text(
        pc1_loading * arrow_scale * 1.1,
        pc2_loading * arrow_scale * 1.1,
        indicator,
        fontsize=8
    )

plt.axhline(0, linewidth=1)
plt.axvline(0, linewidth=1)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA Biplot: Countries and Development Indicators")
plt.grid(True)
plt.tight_layout()
plt.savefig("advanced_pca_biplot.png", dpi=300)
plt.show()

# --------------------------------------------------
# 5. Loading heatmap using matplotlib only
# --------------------------------------------------
selected_components = ["PC1", "PC2", "PC3"]
heatmap_data = loadings[selected_components]

plt.figure(figsize=(9, 7))
plt.imshow(heatmap_data, aspect="auto")

plt.colorbar(label="Loading Value")
plt.xticks(
    ticks=np.arange(len(selected_components)),
    labels=selected_components
)
plt.yticks(
    ticks=np.arange(len(heatmap_data.index)),
    labels=heatmap_data.index
)

plt.title("PCA Loading Heatmap")
plt.tight_layout()
plt.savefig("advanced_pca_loading_heatmap.png", dpi=300)
plt.show()

print("Advanced PCA visuals created successfully.")