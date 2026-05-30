# Constructing-a-Socio-Economic-Development-Index-for-Indian-States-

### The main question of this project is:
Can we use multiple development indicators to create a single data-driven policy priority index for comparing emerging economies?


Instead of judging a countries only on basis of GDP, we combine income, health, education, inflation, unemployment, eloectricity, internet, trade and mortality indicators to understand which countries are doing better and which contries need strong policy attention.

### Reason For This Project

A country may have high GDP but poor education. Another may have good health but weak employment. Another may have high growth but high inflation.

So we wanted we wanted a method to combine many indicators into smaller number of meaningful hidden dimensions 

That is why we selected **PCA(Principal Componebt Analysis)**

PCA helps us answer &\rightarrow$ Out of many indicartors, what are main hidden development patterns

### Why we selected World Bank data

World Bank WDI fits this well because it gives cross-country development indicators. The World Bank also provides an Indicators API, which allows us to access country-level time series data programmatically

So instead of manually downloading messy tables from the website, we used the API.

This made the project more professional because we created a reproducible data pipeline.

### Countries that were slected:
India
China
Brazil
South Africa
Indonesia
Vietnam
Bangladesh
Mexico
Turkey
Malaysia
Thailand
Philippines
Egypt

We selected emerging economies,emerging economies are better because they face similar policy challenges.
**The project focuses on emerging economies because these countries face similar development transitions, making PCA-based comparison more policy-relevant than comparing mixed groups of rich and low-income economies.**

### Selected Year 2010-2023
2010–2023 gives us enough historical coverage to see modern development patterns.
Although the dataset was collected for 2010–2023, the first manual PCA model was implemented on 2022 data to create a clean cross-sectional policy priority index with minimal missing values.

### selected economic indicators.
economic + health + education + infrastructure + digital + trade indicators.

### Why GDP per capita constant 2015 US$ instead of current US$
GDP per capita in constant 2015 US dollars was used to capture real income levels without inflation distortion.

### inflation was still included separately
Inflation was included separately as a macroeconomic stability indicator, while constant GDP per capita captured real income conditions.

### we used secondary school enrollment
Secondary school enrollment was selected because it better captures human capital development beyond basic education access.

### we used ILO modeled unemployment estimate
The modeled ILO unemployment estimate was selected because the project compares multiple countries, requiring internationally comparable labor market data.

### we adjusted “bad when high” indicators
Indicators where higher values represent worse development conditions were multiplied by -1 so that higher values consistently represented better policy conditions.

adjusted inflation = -1 × inflation
adjusted unemployment = -1 × unemployment
adjusted infant mortality = -1 × infant mortality

### Data Pipeline
                                        World Bank API
                                              ↓
                                    Download each indicator
                                              ↓
                        Convert JSON response into pandas DataFrame
                                              ↓
                                  Keep country, year, value
                                              ↓
                            Rename value column based on indicator
                                              ↓
                                Merge all indicators together
                                              ↓
                                        Save final CSV

### Missing value problem
Missing values in secondary school enrollment were handled using country-wise linear interpolation because education indicators generally evolve gradually over time.
| Year | Secondary enrollment |
| ---- | -------------------: |
| 2018 |                   75 |
| 2019 |                   76 |
| 2020 |              missing |
| 2021 |                   78 |

Interpolation estimates 2020 as around 77.
Why is this reasonable?
Because education enrollment usually changes gradually, not randomly overnight.

## Step 1 of PCA:selecting 2022 data:
Why?

Because PCA for country comparison needs one row per country.

If we use many years together, one country appears many times. That is more advanced and can be done later.
| Country | Indicator 1 | Indicator 2 | ... | Indicator 10 |
| ------- | ----------: | ----------: | --: | -----------: |
| India   |       value |       value | ... |        value |
| China   |       value |       value | ... |        value |
| Brazil  |       value |       value | ... |        value |

The 2022 cross-section was selected to construct a latest-year PCA policy index where each country appears once.

## Step 2 of PCA: standardization
Indicators have different units:
GDP per capita = dollars
life expectancy = years
inflation = percent
internet users = percent
infant mortality = per 1000 live births
If we do PCA directly, GDP may dominate because its numbers are very large.

So we standardized each indicator.

$$
Z=\frac{X- \mu}{\sigma}
$$

**All indicators were standardized using z-score normalization to ensure that variables measured in different units contributed fairly to PCA.**

Step 3 of PCA: covariance matrix:
Which indicators move together?
GDP per capita and internet users may move together.
Life expectancy and infant mortality may move in opposite directions.
Electricity access and secondary enrollment may move together.
Inflation and unemployment may indicate macro stress.

$$
C=\frac{1}{n-1} Z^T Z
$$

The covariance matrix was constructed to capture how development indicators vary together across countries.

Step 4 of PCA: eigenvalues and eigenvectors

**Eigenvectors**

Eigenvectors tell us the direction of the principal components.

**Eigenvalues**

Eigenvalues tell us how important each principal component is(ex:A larger eigenvalue means that component explains more information.)

$$
Cv=\lambda v
$$


### PCA result: explained variance insight
The first principal component explains 37.09% of the variance, while the first two components together explain 65.89%. The first three components explain 80.43%, indicating that the selected indicators contain strong common development patterns that can be summarized using a small number of latent dimensions. 


| Component | Explained variance | Cumulative variance |
| --------- | -----------------: | ------------------: |
| PC1       |             37.09% |              37.09% |
| PC2       |             28.79% |              65.89% |
| PC3       |             14.54% |              80.43% |
| PC4       |             10.07% |              90.50% |

### What new insight did PCA give us?
Before PCA, we only had 10 separate indicators.
PC1 = main development/policy capacity dimension
PC2 = second hidden policy dimension
PC3 = additional structural dimension
PCA shows that multi-dimensional development differences can be compressed into a smaller set of interpretable policy dimensions, making comparison easier for decision-makers.

### Step 5 of PCA: loadings

Loadings tell us how strongly each indicator contributes to each principal component.

| Indicator                 | PC1 loading | Meaning            |
| ------------------------- | ----------: | ------------------ |
| GDP per capita            |   **0.439** | strong positive    |
| Life expectancy           |   **0.427** | strong positive    |
| Adjusted infant mortality |   **0.495** | strongest positive |
| Internet users            |   **0.359** | positive           |
| Electricity access        |       0.286 | moderate positive  |
| Trade % GDP               |       0.224 | mild positive      |
| Secondary enrollment      |       0.206 | mild positive      |
| Adjusted inflation        |      -0.203 | mild negative      |
| Adjusted unemployment     |       0.177 | small positive     |
| GDP growth                |      -0.065 | very small         |

PC1 has strong positive loadings on GDP per capita, life expectancy, adjusted infant mortality, internet usage, and electricity access. Since these indicators represent income, health outcomes, child survival, digital readiness, and infrastructure access, PC1 is interpreted as an overall development and policy capacity dimension. Countries with higher PC1 scores have stronger multi-dimensional development performance, while countries with lower PC1 scores represent higher policy priority.

So countries with better combined performance in those indicators move upward.

Countries with lower income, lower digital access, higher infant mortality, or weaker infrastructure move downward.
#### PC2 Interpretation
| Indicator             | PC2 loading | Meaning         |
| --------------------- | ----------: | --------------- |
| Adjusted unemployment |   **0.509** | strong positive |
| Electricity access    |   **0.422** | strong positive |
| GDP growth            |   **0.401** | strong positive |
| Secondary enrollment  |  **-0.452** | strong negative |
| GDP per capita        |      -0.228 | mild negative   |
| Internet users        |      -0.206 | mild negative   |
| Life expectancy       |       0.225 | mild positive   |

PC2 has strong positive loadings on adjusted unemployment, electricity access, and GDP growth, while secondary school enrollment loads negatively. Therefore, PC2 appears to represent a growth-employment-infrastructure contrast rather than a pure development index. It helps distinguish countries based on labor market strength, growth momentum, and infrastructure access relative to education and digital-depth indicators.

#### PC3 interpretation

| Indicator          | PC3 loading | Meaning            |
| ------------------ | ----------: | ------------------ |
| Trade % GDP        |   **0.648** | strongest positive |
| Internet users     |   **0.461** | strong positive    |
| Adjusted inflation |   **0.423** | strong positive    |
| Electricity access |      -0.270 | moderate negative  |
| Life expectancy    |      -0.246 | moderate negative  |
| GDP per capita     |      -0.118 | small negative     |

PC3 is strongly influenced by trade openness, internet usage, and adjusted inflation. This suggests that PC3 captures a trade-digital-macroeconomic stability dimension. It represents a different type of development pattern from PC1, focusing more on openness, connectivity, and price stability.

#### Final component interpretation table

| Principal Component | Main high-loading indicators                                                                   | Interpretation                                |
| ------------------- | ---------------------------------------------------------------------------------------------- | --------------------------------------------- |
| PC1                 | GDP per capita, life expectancy, adjusted infant mortality, internet users, electricity access | **Overall Development and Policy Capacity**   |
| PC2                 | adjusted unemployment, electricity access, GDP growth, negative secondary enrollment           | **Growth–Employment–Infrastructure Contrast** |
| PC3                 | trade, internet users, adjusted inflation                                                      | **Trade–Digital–Macro Stability Dimension**   |



### Step 6 of PCA: country scores
After finding eigenvectors, we projected the standardized country data onto the principal components.

$$
Scores= Zv
$$

Each country has the original indicators:
  GDP per capita
-  GDP growth
-  Adjusted inflation
-  Adjusted unemployment
-  Life expectancy
-  Adjusted infant mortality
-  Secondary enrollment
-  lectricity access
-  Internet users
-  Trade % of GDP

Then PCA adds:

PC1_score
PC2_score
policy_category

| Column            | Meaning                                  |
| ----------------- | ---------------------------------------- |
| `PC1_score`       | Main development / policy capacity score |
| `PC2_score`       | Secondary hidden policy dimension        |
| `policy_category` | Final interpretation group               |

| Rank | Country      | PC1 score | Category                    |
| ---: | ------------ | --------: | --------------------------- |
|    1 | Turkey       |      3.12 | Strong development position |
|    2 | Malaysia     |      2.00 | Strong development position |
|    3 | China        |      1.82 | Strong development position |
|    4 | Thailand     |      1.39 | Strong development position |
|    5 | Mexico       |      1.07 | Strong development position |
|    6 | Brazil       |      0.94 | Moderate / transitional     |
|    7 | Vietnam      |      0.66 | Moderate / transitional     |
|    8 | Indonesia    |     -0.78 | Moderate / transitional     |
|    9 | Egypt        |     -1.26 | High policy priority        |
|   10 | Philippines  |     -1.57 | High policy priority        |
|   11 | India        |     -2.16 | High policy priority        |
|   12 | Bangladesh   |     -2.41 | High policy priority        |
|   13 | South Africa |     -2.81 | High policy priority        |

#### Main insight from PC1 ranking

Among the selected emerging economies, Turkey, Malaysia, China, Thailand, and Mexico appear in the strongest development zone based on the combined structure of income, health, education, infrastructure, digital access, trade, and stability indicators.

#### India is in high policy priority
PC1_score = -2.1617
policy_category = High policy priority

This means India’s combined performance across the selected development indicators is below the PCA average of the selected country group.
| Indicator                 | India value | Possible interpretation                                          |
| ------------------------- | ----------: | ---------------------------------------------------------------- |
| GDP per capita            |     2098.21 | lower income level compared with Turkey, Malaysia, China, Mexico |
| Internet users            |        55.9 | digital access gap compared with stronger countries              |
| Secondary enrollment      |       81.17 | moderate, but lower than Turkey/Malaysia/Brazil/South Africa     |
| Adjusted infant mortality |       -25.7 | infant mortality burden is high compared with stronger countries |
| Trade % GDP               |       50.05 | moderate trade integration                                       |

India’s lower PC1 score appears to be driven by relatively lower GDP per capita, lower internet penetration, and higher infant mortality compared with several emerging-economy peers. This suggests that India’s policy priority areas may include digital inclusion, child health, income productivity, and human capital expansion.

#### Why South Africa is lowest in PC1
| Indicator                 | South Africa |
| ------------------------- | -----------: |
| GDP growth                |         2.05 |
| Adjusted unemployment     |       -32.68 |
| Life expectancy           |        65.45 |
| Electricity access        |         86.5 |
| Infant mortality adjusted |        -24.3 |

South Africa’s low PCA score is strongly linked to labor market stress, lower life expectancy, and weaker electricity access relative to other emerging economies in the sample.

#### Why Turkey is highest

| Indicator            |   Turkey |
| -------------------- | -------: |
| GDP per capita       | 14273.57 |
| Life expectancy      |    77.59 |
| Secondary enrollment |   116.04 |
| Electricity access   |      100 |
| Internet users       |    83.44 |
| Trade % GDP          |    79.89 |

Turkey receives the highest PC1 score because it combines relatively high real GDP per capita, strong secondary enrollment, universal electricity access, high internet penetration, and strong trade openness.

#### PC2 score
| Country      | PC2 score |
| ------------ | --------: |
| Bangladesh   |    2.1365 |
| India        |    1.3499 |
| Egypt        |    0.5957 |
| Thailand     |    0.4507 |
| South Africa |   -4.4103 |
| Turkey       |   -1.8093 |
| Brazil       |   -1.0452 |

PC2 captures a secondary development pattern that is different from the overall development ranking. It may reflect differences in growth, trade, labor market stress, or structural development depending on the indicator loadings.

### Step 7: country ranking
Countries with higher PC1 scores were interpreted as having stronger development and policy capacity, while countries with lower PC1 scores were identified as higher policy priority cases.

### Step 8: policy categories
PC1 >= 1       → Strong development position
-1 to 1        → Moderate / transitional
PC1 < -1       → High policy priority

The PC1 score was translated into policy categories to make the PCA output useful for decision-making.

### What each chart tells you
#### **Scree plot insight**

scree plot should show a sharp drop after PC1–PC3.

The first three PCs are enough to explain most of the structure.

#### **PC1 vs PC2 country map insight**

If countries cluster together:

They have similar development profiles.

If one country is far away:

It may be an outlier with a unique development structure.

#### **Biplot insight**

If country point aligns with education and internet arrows:

It has strong human capital/digital readiness.

If country point is opposite to adjusted unemployment arrow:

It may have labor market stress.

#### **Loading heatmap insight**

If PC1 has high values across human development indicators:

PC1 is development capacity.

If PC2 has trade/growth/inflation patterns:

PC2 is macroeconomic/growth structure.
