import pandas as pd
from pathlib import Path

# ==============================
# STEP 1: READ ALL CSV FILES
# ==============================

data_folder = Path("data")

dfs = []
for file in data_folder.glob("*.csv"):
    print(f"Reading file: {file}")
    df = pd.read_csv(file)
    dfs.append(df)

# Combine all CSVs
df = pd.concat(dfs, ignore_index=True)

# ==============================
# STEP 2: NORMALISE COLUMN NAMES
# ==============================

df.columns = df.columns.str.lower().str.strip()

# ==============================
# STEP 3: FILTER PINK MORSEL (ROBUST)
# ==============================

# Handles:
# pink morsel
# Pink Morsel
# pink morsels (if ever appears)
df["product"] = df["product"].astype(str).str.lower().str.strip()

df = df[df["product"].str.contains("pink morsel", na=False)]

print("Rows after product filter:", len(df))

# ==============================
# STEP 4: CLEAN NUMERIC COLUMNS
# ==============================

# Quantity
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

# Price: remove $ and convert
df["price"] = (
    df["price"]
    .astype(str)
    .str.replace("$", "", regex=False)
)

df["price"] = pd.to_numeric(df["price"], errors="coerce")

# Drop invalid rows
df = df.dropna(subset=["quantity", "price"])

print("Rows after numeric cleaning:", len(df))

# ==============================
# STEP 5: CREATE SALES (NUMERIC)
# ==============================

df["sales"] = df["quantity"] * df["price"]

# ==============================
# STEP 6: FINAL OUTPUT COLUMNS
# ==============================

df = df[["sales", "date", "region"]]

# ==============================
# STEP 7: SAVE OUTPUT
# ==============================

df.to_csv("output.csv", index=False)

print("✅ output.csv generated successfully")
print("Rows written:", len(df))
print(df.head())
