import pandas as pd
df = pd.read_csv("data/world-data-2023.csv")
print(df.head())
df_clean = df.copy()
print(df_clean.info())
print(df_clean.shape)
print(df_clean.isnull().sum())
pourcentage_nan = (df_clean.isnull().sum() / len(df_clean)) * 100
print(pourcentage_nan.sort_values(ascending=False))
df_clean.columns = (
    df_clean.columns
    .str.lower()
    .str.strip()
    .str.replace(" ", "")
)
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)
# Colonnes numériques
df = df.fillna(df.select_dtypes(include="number").mean())
df = df.dropna()
df["GDP"] = pd.to_numeric(df["GDP"], errors="coerce")
print(df.info())
print(df.isnull().sum())
df.to_csv("data/world-data-2023-clean.csv", index=False)
