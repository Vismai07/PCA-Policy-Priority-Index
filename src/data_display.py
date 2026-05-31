import pandas as pd

# Step 1: Read the CSV file
df = pd.read_csv("worldbank_pca_policy_data_2010_2023.csv")

# Step 2: Show all columns properly
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

# Step 3: Display first 10 rows
print("\nFIRST 10 ROWS:")
print(df.head(10))

# Step 4: Display number of rows and columns
print("\nDATASET SHAPE:")
print(df.shape)

# Step 5: Display column names
print("\nCOLUMN NAMES:")
for col in df.columns:
    print(col)

# Step 6: Display missing values in each column
print("\nMISSING VALUES:")
print(df.isnull().sum())

# Step 7: Display data types
print("\nDATA TYPES:")
print(df.dtypes)