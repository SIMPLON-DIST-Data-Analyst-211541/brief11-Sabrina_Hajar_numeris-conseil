# ==========================================================
# NETTOYAGE DES DONNÉES - WORLD DATA 2023
# ==========================================================

from pathlib import Path
import pandas as pd

# ==========================================================
# Chargement du dataset
# ==========================================================

# Compatible Jupyter Notebook / Google Colab
BASE_DIR = Path.cwd()

# Le fichier est normalement dans le dossier data
csv_path = BASE_DIR / "data" / "world-data-2023.csv"

# Si le dossier data n'existe pas, chercher dans le dossier courant
if not csv_path.exists():
    csv_path = BASE_DIR / "world-data-2023.csv"

# Chargement
df = pd.read_csv(csv_path)

# ==========================================================
# CONVERSION DES VARIABLES NUMÉRIQUES
# ==========================================================

colonnes_numeriques = [
    "Density_P_Km2",
    "Agricultural_Land_pct",
    "Land_AreaKm2",
    "Armed_Forces_size",
    "Co2-Emissions",
    "CPI",
    "CPI_Change_pct",
    "Forested_Area_pct",
    "Gasoline_Price",
    "GDP",
    "Gross_primary_education_enrollment_pct",
    "Gross_tertiary_education_enrollment_pct",
    "Minimum_wage",
    "Out_of_pocket_health_expenditure",
    "Population",
    "Population:_Labor_force_participation_pct",
    "Tax_revenue_pct",
    "Total_tax_rate",
    "Unemployment_rate",
    "Urban_population",
    "Birth_Rate",
    "Calling_Code",
    "Fertility_Rate",
    "Infant_mortality",
    "Life_expectancy",
    "Maternal_mortality_ratio",
    "Physicians_per_thousand",
    "Latitude",
    "Longitude"
]

for col in colonnes_numeriques:

    if col in df.columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.replace("Unknown", "", regex=False)
            .str.strip()
        )

        df[col] = pd.to_numeric(df[col], errors="coerce")

# Remplacer les NaN numériques par la médiane

for col in colonnes_numeriques:

    if col in df.columns:

        df[col] = df[col].fillna(df[col].median())

df["GDP_per_capita"] = df["GDP"] / df["Population"]

# ==========================================================
# Conversion explicite de la colonne Population
# ==========================================================

if "Population" in df.columns:
    df["Population"] = (
        df["Population"]
        .astype(str)
        .str.replace(",", "", regex=False)
    )

    df["Population"] = pd.to_numeric(df["Population"], errors="coerce")

print("Type de Population :", df["Population"].dtype)

# ==========================================================
# Diagnostic initial
# ==========================================================

print("=" * 60)
print("DIAGNOSTIC INITIAL")
print("=" * 60)

print("Dimensions :", df.shape)
print("Doublons :", df.duplicated().sum())

print("\nValeurs manquantes :")
print(df.isnull().sum())

print("\nRésumé statistique :")
print(df.describe(include="all"))

# ==========================================================
# Renommage des colonnes
# ==========================================================

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

# ==========================================================
# Suppression des doublons
# ==========================================================

df = df.drop_duplicates()

if "Country" in df.columns:
    print("\nPays dupliqués :", df["Country"].duplicated().sum())

# ==========================================================
# Nettoyage des colonnes numériques
# ==========================================================

def nettoyer_numerique(colonne):

    propre = (
        colonne.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.replace("€", "", regex=False)
        .str.strip()
    )

    return pd.to_numeric(propre, errors="coerce")


for col in df.columns:

    if df[col].dtype == "object":

        conversion = nettoyer_numerique(df[col])

        # On convertit uniquement si au moins 70 % des valeurs sont numériques
        if conversion.notna().sum() >= len(df) * 0.70:
            df[col] = conversion

# ==========================================================
# Vérification des types
# ==========================================================

print("\nTypes des variables :")
print(df.dtypes)

# ==========================================================
# Traitement des valeurs manquantes
# ==========================================================

# Colonnes numériques
num_cols = df.select_dtypes(include=["number"]).columns

for col in num_cols:
    df[col] = df[col].fillna(df[col].median())

# Colonnes texte
text_cols = df.select_dtypes(include="object").columns

for col in text_cols:
    df[col] = df[col].str.strip().fillna("Unknown")

# ==========================================================
# Vérification finale des valeurs manquantes
# ==========================================================

print("\nValeurs manquantes restantes :")
print(df.isnull().sum())

print("\nTotal :", df.isnull().sum().sum())

# ==========================================================
# Détection des valeurs aberrantes (IQR)
# ==========================================================

print("\n==============================")
print("VALEURS ABERRANTES")
print("==============================")

for col in num_cols:

    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)

    IQR = Q3 - Q1

    borne_inf = Q1 - 1.5 * IQR
    borne_sup = Q3 + 1.5 * IQR

    outliers = df[
        (df[col] < borne_inf) |
        (df[col] > borne_sup)
    ]

    print(f"\n{col}")
    print(f"Nombre de valeurs aberrantes : {len(outliers)}")
    print(f"Borne inférieure : {borne_inf:.2f}")
    print(f"Borne supérieure : {borne_sup:.2f}")

print("\nLes valeurs aberrantes sont conservées car elles représentent des situations réelles de certains pays.")

# ==========================================================
# Contrôle final
# ==========================================================

print("\n==============================")
print("CONTRÔLE FINAL")
print("==============================")

print(df.shape)

print("\nInformations générales")
df.info()

print("\nRésumé statistique")
print(df.describe())

print("\nValeurs manquantes")
print(df.isnull().sum())

# ==========================================================
# Sauvegarde
# ==========================================================

output_path = BASE_DIR / "world-data-2023-clean.csv"

df.to_csv(output_path, index=False)

print("\nDataset nettoyé enregistré avec succès.")
print("Emplacement :", output_path)