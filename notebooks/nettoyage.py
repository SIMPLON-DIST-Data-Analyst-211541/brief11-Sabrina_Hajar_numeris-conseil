# Installer les bibliothèques
# Dans le terminal de VS Code : pip install pandas, matplotlib, seaborn, numpy

# Charger le dataset
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data" / "world-data-2023.csv"

df = pd.read_csv(csv_path)

# Aperçu
print(df.head())
print(df.info())

# Vérifier les valeurs manquantes

print(df.isnull().sum())

# Renommer les colonnes

df.columns = (
    df.columns
      .str.strip()
      .str.replace("\n", "_")
      .str.replace(" ", "_")
      .str.replace("(", "", regex=False)
      .str.replace(")", "", regex=False)
      .str.replace("%", "pct", regex=False)
      .str.replace("/", "_", regex=False)
)

print(df.columns)

# Supprimer les doublons

df = df.drop_duplicates()

# Nettoyer les colonnes numériques
# Plusieurs colonnes sont au format texte à cause des virgules, $, etc.

cols = [
    "Density_P_Km2",
    "Land_AreaKm2",
    "GDP",
    "Population",
    "Co2-Emissions",
    "Minimum_wage",
    "Gasoline_Price",
    "CPI"
]

for col in cols:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Traiter les valeurs manquantes
# Pour les colonnes numériques :

num_cols = df.select_dtypes(include="number").columns

for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

# Pour les colonnes texte :

obj_cols = df.select_dtypes(include="object").columns

for col in obj_cols:
    df[col] = df[col].fillna("Unknown")

# Vérifier les types

print(df.dtypes)

# Sauvegarder le dataset nettoyé

df.to_csv("world-data-2023-clean.csv", index=False)

print("Dataset nettoyé enregistré avec succès.")

# Contrôles finaux

print(df.shape)
print(df.info())
print(df.describe())
print(df.isnull().sum())
