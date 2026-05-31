import pandas as pd
import requests
from functools import reduce

# --------------------------------------------------
# 1. Countries
# --------------------------------------------------
countries = "IND;CHN;BRA;ZAF;IDN;VNM;BGD;MEX;TUR;MYS;THA;PHL;EGY"

# --------------------------------------------------
# 2. Indicators for your PCA policy/economics project
# --------------------------------------------------
indicators = {
    "NY.GDP.PCAP.KD": "gdp_per_capita_constant_2015_usd",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth_annual_pct",
    "FP.CPI.TOTL.ZG": "inflation_annual_pct",
    "SL.UEM.TOTL.ZS": "unemployment_total_pct_ilo_estimate",
    "SP.DYN.LE00.IN": "life_expectancy_years",
    "SP.DYN.IMRT.IN": "infant_mortality_per_1000_live_births",
    "SE.SEC.ENRR": "secondary_school_enrollment_gross_pct",
    "EG.ELC.ACCS.ZS": "access_to_electricity_pct_population",
    "IT.NET.USER.ZS": "individuals_using_internet_pct_population",
    "NE.TRD.GNFS.ZS": "trade_pct_gdp"
}

# --------------------------------------------------
# 3. Function to download one indicator
# --------------------------------------------------
def get_worldbank_indicator(indicator_code, indicator_name):
    url = (
        f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator_code}"
        f"?format=json&date=2010:2023&per_page=20000"
    )

    response = requests.get(url)
    data = response.json()

    # World Bank API returns data in data[1]
    records = data[1]

    df = pd.DataFrame(records)

    df = df[["countryiso3code", "country", "date", "value"]]

    # Extract country name from dictionary
    df["country"] = df["country"].apply(lambda x: x["value"])

    df.rename(
        columns={
            "countryiso3code": "country_code",
            "date": "year",
            "value": indicator_name
        },
        inplace=True
    )

    df["year"] = df["year"].astype(int)

    return df


# --------------------------------------------------
# 4. Download all indicators one by one
# --------------------------------------------------
all_dataframes = []

for code, name in indicators.items():
    print(f"Downloading: {name}")
    df_indicator = get_worldbank_indicator(code, name)
    all_dataframes.append(df_indicator)


# --------------------------------------------------
# 5. Combine all indicators into one dataset
# --------------------------------------------------
combined_df = reduce(
    lambda left, right: pd.merge(
        left,
        right,
        on=["country_code", "country", "year"],
        how="outer"
    ),
    all_dataframes
)

# Sort neatly
combined_df = combined_df.sort_values(["country", "year"])

# --------------------------------------------------
# 6. Convert indicator columns to numeric
# --------------------------------------------------
for col in indicators.values():
    combined_df[col] = pd.to_numeric(combined_df[col], errors="coerce")


# --------------------------------------------------
# 7. Create adjusted columns for bad indicators
# Higher inflation, unemployment, and infant mortality are bad
# So we multiply by -1 for PCA interpretation
# --------------------------------------------------
combined_df["adjusted_inflation_annual_pct"] = -1 * combined_df["inflation_annual_pct"]
combined_df["adjusted_unemployment_total_pct_ilo_estimate"] = -1 * combined_df["unemployment_total_pct_ilo_estimate"]
combined_df["adjusted_infant_mortality_per_1000_live_births"] = -1 * combined_df["infant_mortality_per_1000_live_births"]


# --------------------------------------------------
# 8. Save final combined dataset
# --------------------------------------------------
combined_df.to_csv("worldbank_pca_policy_data_2010_2023.csv", index=False)

print("Data combined successfully.")
print(combined_df.head())
print(combined_df.shape)