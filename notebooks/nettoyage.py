from pathlib import Path
import pandas as pd

# Racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Lecture du fichier CSV
csv_path = BASE_DIR / "data" / "world-data-2023.csv"

print("Lecture du fichier :", csv_path)

df = pd.read_csv(csv_path)

df_clean = df.copy()

# ==========================
# 2. Nettoyage des noms de colonnes
# ==========================
df_clean.columns = (
    df_clean.columns
    .str.replace("\n", " ", regex=False)
    .str.lower()
    .str.strip()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

# ==========================
# 3. Suppression des espaces
# ==========================
for col in df_clean.select_dtypes(include=["object"]).columns:
    df_clean[col] = df_clean[col].str.strip()

# ==========================
# 4. Conversion automatique
#    des colonnes numériques
# ==========================
for col in df_clean.select_dtypes(include=["object"]).columns:

    temp = (
        df_clean[col]
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("%", "", regex=False)
    )

    numeric = pd.to_numeric(temp, errors="coerce")

    # On convertit seulement si la majorité des valeurs sont numériques
    if numeric.notna().sum() >= len(df_clean) * 0.5:
        df_clean[col] = numeric

# ==========================
# 5. Remplacement des NaN
#    uniquement dans les
#    colonnes numériques
# ==========================
numeric_cols = df_clean.select_dtypes(include="number").columns

df_clean[numeric_cols] = (
    df_clean[numeric_cols]
    .fillna(df_clean[numeric_cols].median())
)

# ==========================
# 6. Vérification
# ==========================
print(df_clean.info())

print("\nValeurs manquantes :")
print(df_clean.isna().sum())

print("\nDimensions :", df_clean.shape)

# ==========================
# 7. Sauvegarde
# ==========================
df_clean.to_csv("world-data-2023-clean.csv", index=False)

print("\nFichier enregistré : world-data-2023-clean.csv")

from pathlib import Path
import pandas as pd

# Racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Lecture du fichier brut
df = pd.read_csv(BASE_DIR / "data" / "world-data-2023.csv")

# Copie
df_clean = df.copy()

# ... ton nettoyage ...

# Sauvegarde
output_path = BASE_DIR / "data" / "world-data-2023-clean.csv"

df_clean.to_csv(output_path, index=False)

print("Fichier enregistré :", output_path)