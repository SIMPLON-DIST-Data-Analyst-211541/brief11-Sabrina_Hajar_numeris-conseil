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
# 2. Suppression des espaces
# ==========================================================

for col in df_clean.select_dtypes(include="object").columns:
    df_clean[col] = df_clean[col].str.strip()

# ==========================================================
# 3. Conversion des colonnes numériques
# ==========================================================

for col in df_clean.select_dtypes(include="object").columns:

    temp = (
        df_clean[col]
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("%", "", regex=False)
    )

    numeric = pd.to_numeric(temp, errors="coerce")

    # Conversion uniquement si la majorité des valeurs est numérique
    if numeric.notna().sum() >= len(df_clean) * 0.5:
        df_clean[col] = numeric

# ==========================================================
# 4. Remplacement des valeurs manquantes
# ==========================================================

numeric_cols = df_clean.select_dtypes(include="number").columns

df_clean[numeric_cols] = (
    df_clean[numeric_cols]
    .fillna(df_clean[numeric_cols].median())
)

# ==========================================================
# 5. Vérifications
# ==========================================================

print(df_clean.info())

print("\nValeurs manquantes :")
print(df_clean.isna().sum())

print("\nDimensions :", df_clean.shape)

# ==========================================================
# 6. Sauvegarde
# ==========================================================

output_path = BASE_DIR / "data" / "world-data-2023-clean.csv"

df_clean.to_csv(output_path, index=False)

print("\nFichier enregistré :", output_path)