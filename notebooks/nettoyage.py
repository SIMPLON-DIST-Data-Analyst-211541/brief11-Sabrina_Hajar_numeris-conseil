from pathlib import Path
import pandas as pd

# ==========================================================
# NETTOYAGE DU DATASET WORLD DATA 2023
# ==========================================================

# Racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Lecture du fichier brut
input_path = BASE_DIR / "data" / "world-data-2023.csv"

print("Lecture du fichier :", input_path)

df = pd.read_csv(input_path)

# Copie du DataFrame
df_clean = df.copy()

# ==========================================================
# 1. Nettoyage des noms de colonnes
# ==========================================================

df_clean.columns = (
    df_clean.columns
    .str.replace("\n", " ", regex=False)
    .str.lower()
    .str.strip()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

# ==========================================================
# 2. Suppression de la colonne abbreviation
# ==========================================================

df_clean = df_clean.drop(columns=["abbreviation"], errors="ignore")

# ==========================================================
# 3. Suppression des espaces
# ==========================================================

for col in df_clean.select_dtypes(include="object").columns:
    df_clean[col] = df_clean[col].str.strip()

# ==========================================================
# 4. Détection des caractères mal encodés
# ==========================================================

print("\n===== CARACTÈRES MAL ENCODÉS =====")

for col in df_clean.select_dtypes(include="object"):
    erreurs = df_clean[df_clean[col].str.contains("�", na=False)]

    if not erreurs.empty:
        print(f"\nColonne : {col}")
        print(erreurs[[col]])

# ==========================================================
# 5. Correction des caractères mal encodés
# ==========================================================

corrections = {
    "Bras���": "Brasília",
    "Bogot�": "Bogotá",
    "San Jos������": "San José",
    "Reykjav��": "Reykjavík",
    "Mal�": "Malé",
    "Chi����": "Chișinău",
    "Asunci��": "Asunción",
    "Lom�": "Lomé",
    "Nuku����": "Nukuʻalofa",
    "S�����������": "São Tomé and Príncipe"
}

for col in ["capital_major_city", "largest_city", "country"]:
    if col in df_clean.columns:
        df_clean[col] = df_clean[col].replace(corrections)

# ==========================================================
# 6. Vérification qu'il ne reste plus d'erreurs
# ==========================================================

print("\n===== VÉRIFICATION =====")

for col in df_clean.select_dtypes(include="object"):
    nb = df_clean[col].astype(str).str.contains("�", na=False).sum()
    print(f"{col} : {nb}")

# ==========================================================
# 7. Conversion des colonnes numériques
# ==========================================================

for col in df_clean.select_dtypes(include="object"):

    temp = (
        df_clean[col]
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("%", "", regex=False)
    )

    numeric = pd.to_numeric(temp, errors="coerce")

    if numeric.notna().sum() >= len(df_clean) * 0.5:
        df_clean[col] = numeric

# ==========================================================
# 8. Valeurs manquantes
# ==========================================================

print("\nValeurs manquantes :")
print(df_clean.isna().sum())

print("\nLignes contenant des valeurs manquantes :")
print(df_clean[df_clean.isna().any(axis=1)])

colonnes = [
    "currency_code",
    "official_language",
    "capital_major_city",
    "largest_city"
]

df_clean[colonnes] = df_clean[colonnes].fillna("Unknown")

numeric_cols = df_clean.select_dtypes(include="number").columns

df_clean[numeric_cols] = (
    df_clean[numeric_cols]
    .fillna(df_clean[numeric_cols].median())
)

# ==========================================================
# 9. Vérification des doublons
# ==========================================================

print("\nNombre de doublons :", df_clean.duplicated().sum())

# ==========================================================
# 10. Recherche des valeurs aberrantes (IQR)
# ==========================================================

print("\n===== VALEURS ABERRANTES =====")

colonnes_num = df_clean.select_dtypes(include="number").columns

for col in colonnes_num:

    Q1 = df_clean[col].quantile(0.25)
    Q3 = df_clean[col].quantile(0.75)
    IQR = Q3 - Q1

    borne_inf = Q1 - 1.5 * IQR
    borne_sup = Q3 + 1.5 * IQR

    nb = ((df_clean[col] < borne_inf) | (df_clean[col] > borne_sup)).sum()

    print(f"{col} : {nb} valeur(s) aberrante(s)")