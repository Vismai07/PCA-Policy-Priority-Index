import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --------------------------------------------------
# INTERACTIVE QUANT-STYLE 3D PCA VISUALIZATION
# Manual PCA, no sklearn PCA used
# --------------------------------------------------

# --------------------------------------------------
# 1. Load cleaned World Bank data
# --------------------------------------------------
df = pd.read_csv("worldbank_pca_policy_data_cleaned.csv")

# --------------------------------------------------
# 2. Select indicators for PCA
# We use adjusted versions for bad-when-high indicators.
# Higher value should mean better development condition.
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

# --------------------------------------------------
# 3. Keep country-year observations
# This gives a richer cloud than only one year.
# --------------------------------------------------
pca_df = df[["country_code", "country", "year"] + pca_columns].copy()

# Drop rows with missing values
pca_df = pca_df.dropna().reset_index(drop=True)

print("PCA panel shape:", pca_df.shape)

# --------------------------------------------------
# 4. Manual standardization
# Formula:
# Z = (X - mean) / standard deviation
# --------------------------------------------------
X = pca_df[pca_columns].values

mean_values = np.mean(X, axis=0)
std_values = np.std(X, axis=0, ddof=1)

Z = (X - mean_values) / std_values

# --------------------------------------------------
# 5. Manual covariance matrix
# Formula:
# C = (Z.T @ Z) / (n - 1)
# --------------------------------------------------
n = Z.shape[0]
cov_matrix = (Z.T @ Z) / (n - 1)

# --------------------------------------------------
# 6. Eigen decomposition
# Formula:
# C v = lambda v
# --------------------------------------------------
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

# Remove tiny imaginary numerical noise
eigenvalues = eigenvalues.real
eigenvectors = eigenvectors.real

# --------------------------------------------------
# 7. Sort eigenvalues/eigenvectors from largest to smallest
# --------------------------------------------------
sorted_indices = np.argsort(eigenvalues)[::-1]

eigenvalues_sorted = eigenvalues[sorted_indices]
eigenvectors_sorted = eigenvectors[:, sorted_indices]

# --------------------------------------------------
# 8. Explained variance
# --------------------------------------------------
explained_variance_ratio = eigenvalues_sorted / np.sum(eigenvalues_sorted)
cumulative_variance = np.cumsum(explained_variance_ratio)

explained_variance_df = pd.DataFrame({
    "principal_component": [f"PC{i+1}" for i in range(len(pca_columns))],
    "eigenvalue": eigenvalues_sorted,
    "explained_variance_ratio": explained_variance_ratio,
    "cumulative_variance": cumulative_variance
})

explained_variance_df.to_csv("interactive_pca_explained_variance_panel.csv", index=False)

# --------------------------------------------------
# 9. PCA scores
# Formula:
# Scores = Z @ eigenvectors
# --------------------------------------------------
scores = Z @ eigenvectors_sorted

pca_df["PC1"] = scores[:, 0]
pca_df["PC2"] = scores[:, 1]
pca_df["PC3"] = scores[:, 2]

# --------------------------------------------------
# 10. PCA loadings
# Loadings show direction of each indicator in PCA space.
# --------------------------------------------------
loadings = pd.DataFrame(
    eigenvectors_sorted,
    index=pca_columns,
    columns=[f"PC{i+1}" for i in range(len(pca_columns))]
)

# --------------------------------------------------
# 11. Fix direction of PC1
# If GDP loading is negative, flip PC1 direction.
# This makes high PC1 easier to interpret as stronger development.
# --------------------------------------------------
if loadings.loc["gdp_per_capita_constant_2015_usd", "PC1"] < 0:
    pca_df["PC1"] = -1 * pca_df["PC1"]
    loadings["PC1"] = -1 * loadings["PC1"]

# Save PCA outputs
pca_df.to_csv("interactive_pca_panel_scores.csv", index=False)
loadings.to_csv("interactive_pca_panel_loadings.csv")

# --------------------------------------------------
# 12. Policy zone based on PC1
# These are visual categories for the graph.
# --------------------------------------------------
q_low = pca_df["PC1"].quantile(0.33)
q_high = pca_df["PC1"].quantile(0.67)

def policy_zone(score):
    if score >= q_high:
        return "Strong development zone"
    elif score <= q_low:
        return "High policy priority zone"
    else:
        return "Transitional zone"

pca_df["policy_zone"] = pca_df["PC1"].apply(policy_zone)

# --------------------------------------------------
# 13. Build custom hover text
# --------------------------------------------------
hover_text = []

for _, row in pca_df.iterrows():
    text = (
        f"<b>{row['country']}</b><br>"
        f"Year: {int(row['year'])}<br><br>"
        f"PC1: {row['PC1']:.3f}<br>"
        f"PC2: {row['PC2']:.3f}<br>"
        f"PC3: {row['PC3']:.3f}<br><br>"
        f"Policy Zone: {row['policy_zone']}<br><br>"
        f"GDP per capita: {row['gdp_per_capita_constant_2015_usd']:.2f}<br>"
        f"GDP growth: {row['gdp_growth_annual_pct']:.2f}<br>"
        f"Inflation adjusted: {row['adjusted_inflation_annual_pct']:.2f}<br>"
        f"Unemployment adjusted: {row['adjusted_unemployment_total_pct_ilo_estimate']:.2f}<br>"
        f"Life expectancy: {row['life_expectancy_years']:.2f}<br>"
        f"Internet users: {row['individuals_using_internet_pct_population']:.2f}"
    )
    hover_text.append(text)

pca_df["hover_text"] = hover_text

# --------------------------------------------------
# 14. Create interactive 3D scatter cloud
# --------------------------------------------------
fig = go.Figure()

zone_colors = {
    "Strong development zone": "#00F5D4",
    "Transitional zone": "#FEE440",
    "High policy priority zone": "#F15BB5"
}

for zone, color in zone_colors.items():
    temp = pca_df[pca_df["policy_zone"] == zone]

    fig.add_trace(
        go.Scatter3d(
            x=temp["PC1"],
            y=temp["PC2"],
            z=temp["PC3"],
            mode="markers",
            name=zone,
            text=temp["hover_text"],
            hoverinfo="text",
            marker=dict(
                size=5,
                color=color,
                opacity=0.82,
                line=dict(width=0.4, color="white")
            )
        )
    )

# --------------------------------------------------
# 15. Add country trajectory lines over time
# This makes the graph more dynamic and quant-style.
# --------------------------------------------------
for country in pca_df["country"].unique():
    temp = pca_df[pca_df["country"] == country].sort_values("year")

    fig.add_trace(
        go.Scatter3d(
            x=temp["PC1"],
            y=temp["PC2"],
            z=temp["PC3"],
            mode="lines",
            name=f"{country} trajectory",
            showlegend=False,
            line=dict(
                width=2,
                color="rgba(180,180,180,0.35)"
            ),
            hoverinfo="skip"
        )
    )

# --------------------------------------------------
# 16. Add PCA loading arrows
# Arrows show which indicators pull the PCA space.
# --------------------------------------------------
max_range = max(
    pca_df["PC1"].abs().max(),
    pca_df["PC2"].abs().max(),
    pca_df["PC3"].abs().max()
)

arrow_scale = max_range * 0.85

short_labels = {
    "gdp_per_capita_constant_2015_usd": "GDP/capita",
    "gdp_growth_annual_pct": "GDP growth",
    "adjusted_inflation_annual_pct": "Low inflation",
    "adjusted_unemployment_total_pct_ilo_estimate": "Low unemployment",
    "life_expectancy_years": "Life expectancy",
    "adjusted_infant_mortality_per_1000_live_births": "Low infant mortality",
    "secondary_school_enrollment_gross_pct": "Secondary enrollment",
    "access_to_electricity_pct_population": "Electricity access",
    "individuals_using_internet_pct_population": "Internet users",
    "trade_pct_gdp": "Trade openness"
}

for indicator in loadings.index:
    x_end = loadings.loc[indicator, "PC1"] * arrow_scale
    y_end = loadings.loc[indicator, "PC2"] * arrow_scale
    z_end = loadings.loc[indicator, "PC3"] * arrow_scale

    # Arrow line
    fig.add_trace(
        go.Scatter3d(
            x=[0, x_end],
            y=[0, y_end],
            z=[0, z_end],
            mode="lines",
            name=short_labels[indicator],
            line=dict(
                width=6,
                color="#FFFFFF"
            ),
            hovertext=f"{short_labels[indicator]} loading vector",
            hoverinfo="text",
            showlegend=False
        )
    )

    # Arrow tip using cone
    fig.add_trace(
        go.Cone(
            x=[x_end],
            y=[y_end],
            z=[z_end],
            u=[x_end],
            v=[y_end],
            w=[z_end],
            sizemode="absolute",
            sizeref=0.18,
            anchor="tip",
            colorscale=[[0, "#FFFFFF"], [1, "#FFFFFF"]],
            showscale=False,
            hoverinfo="skip",
            showlegend=False
        )
    )

    # Arrow label
    fig.add_trace(
        go.Scatter3d(
            x=[x_end * 1.12],
            y=[y_end * 1.12],
            z=[z_end * 1.12],
            mode="text",
            text=[short_labels[indicator]],
            textfont=dict(
                size=11,
                color="#FFFFFF"
            ),
            hoverinfo="skip",
            showlegend=False
        )
    )

# --------------------------------------------------
# 17. Add transparent variance ellipsoid
# This gives a quant/research visualization feel.
# --------------------------------------------------
theta = np.linspace(0, 2 * np.pi, 60)
phi = np.linspace(0, np.pi, 30)

theta, phi = np.meshgrid(theta, phi)

# Ellipsoid radii based on PC score standard deviation
rx = pca_df["PC1"].std() * 2.0
ry = pca_df["PC2"].std() * 2.0
rz = pca_df["PC3"].std() * 2.0

x_ellipsoid = rx * np.cos(theta) * np.sin(phi)
y_ellipsoid = ry * np.sin(theta) * np.sin(phi)
z_ellipsoid = rz * np.cos(phi)

fig.add_trace(
    go.Surface(
        x=x_ellipsoid,
        y=y_ellipsoid,
        z=z_ellipsoid,
        opacity=0.12,
        showscale=False,
        colorscale=[[0, "#4361EE"], [1, "#7209B7"]],
        name="PCA variance envelope",
        hoverinfo="skip"
    )
)

# --------------------------------------------------
# 18. Add origin axes
# --------------------------------------------------
axis_len = max_range * 1.2

fig.add_trace(
    go.Scatter3d(
        x=[-axis_len, axis_len],
        y=[0, 0],
        z=[0, 0],
        mode="lines",
        line=dict(color="rgba(255,255,255,0.35)", width=3),
        showlegend=False,
        hoverinfo="skip"
    )
)

fig.add_trace(
    go.Scatter3d(
        x=[0, 0],
        y=[-axis_len, axis_len],
        z=[0, 0],
        mode="lines",
        line=dict(color="rgba(255,255,255,0.35)", width=3),
        showlegend=False,
        hoverinfo="skip"
    )
)

fig.add_trace(
    go.Scatter3d(
        x=[0, 0],
        y=[0, 0],
        z=[-axis_len, axis_len],
        mode="lines",
        line=dict(color="rgba(255,255,255,0.35)", width=3),
        showlegend=False,
        hoverinfo="skip"
    )
)

# --------------------------------------------------
# 19. Layout: high-fi quant dashboard style
# --------------------------------------------------
pc1_var = explained_variance_ratio[0] * 100
pc2_var = explained_variance_ratio[1] * 100
pc3_var = explained_variance_ratio[2] * 100
pc123_var = cumulative_variance[2] * 100

fig.update_layout(
    title=dict(
        text=(
            "Interactive 3D PCA Development Space<br>"
            f"<sup>Manual PCA on World Bank Indicators | "
            f"PC1={pc1_var:.2f}%, PC2={pc2_var:.2f}%, PC3={pc3_var:.2f}% "
            f"| Total captured={pc123_var:.2f}%</sup>"
        ),
        x=0.5,
        font=dict(size=22, color="white")
    ),
    template="plotly_dark",
    paper_bgcolor="#050816",
    plot_bgcolor="#050816",
    legend=dict(
        x=0.02,
        y=0.98,
        bgcolor="rgba(0,0,0,0.25)",
        bordercolor="rgba(255,255,255,0.2)",
        borderwidth=1,
        font=dict(color="white")
    ),
    scene=dict(
        bgcolor="#050816",
        xaxis=dict(
            title=f"PC1: Development Capacity ({pc1_var:.2f}%)",
            gridcolor="rgba(255,255,255,0.12)",
            zerolinecolor="rgba(255,255,255,0.35)",
            showbackground=True,
            backgroundcolor="rgba(255,255,255,0.03)"
        ),
        yaxis=dict(
            title=f"PC2: Secondary Policy Dimension ({pc2_var:.2f}%)",
            gridcolor="rgba(255,255,255,0.12)",
            zerolinecolor="rgba(255,255,255,0.35)",
            showbackground=True,
            backgroundcolor="rgba(255,255,255,0.03)"
        ),
        zaxis=dict(
            title=f"PC3: Structural Development Dimension ({pc3_var:.2f}%)",
            gridcolor="rgba(255,255,255,0.12)",
            zerolinecolor="rgba(255,255,255,0.35)",
            showbackground=True,
            backgroundcolor="rgba(255,255,255,0.03)"
        ),
        camera=dict(
            eye=dict(x=1.65, y=1.65, z=1.25)
        )
    ),
    margin=dict(l=0, r=0, b=0, t=80),
    width=1200,
    height=850
)

# --------------------------------------------------
# 20. Save interactive HTML
# --------------------------------------------------
fig.write_html("interactive_quant_pca_3d.html")

print("Interactive quant-style PCA 3D graph created:")
print("interactive_quant_pca_3d.html")

print("\nExplained variance:")
print(explained_variance_df.head(5))

print("\nFiles saved:")
print("interactive_quant_pca_3d.html")
print("interactive_pca_panel_scores.csv")
print("interactive_pca_panel_loadings.csv")
print("interactive_pca_explained_variance_panel.csv")