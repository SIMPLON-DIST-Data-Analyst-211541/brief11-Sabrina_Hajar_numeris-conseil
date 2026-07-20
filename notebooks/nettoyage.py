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

# Corriger le nom du pays avant le reste
mask = df_clean["country"].astype(str).str.contains("�", na=False)
df_clean.loc[mask, "country"] = "São Tomé and Príncipe"

# Corrections par pays
corrections = {
    "Brazil": {
        "capital_major_city": "Brasília",
        "largest_city": "São Paulo"
    },
    "Cameroon": {
        "capital_major_city": "Yaoundé"
    },
    "Colombia": {
        "capital_major_city": "Bogotá",
        "largest_city": "Bogotá"
    },
    "Costa Rica": {
        "capital_major_city": "San José",
        "largest_city": "San José"
    },
    "Cyprus": {
        "largest_city": "Strovolos"
    },
    "Iceland": {
        "capital_major_city": "Reykjavík",
        "largest_city": "Reykjavík"
    },
    "Maldives": {
        "capital_major_city": "Malé",
        "largest_city": "Malé"
    },
    "Moldova": {
        "capital_major_city": "Chișinău",
        "largest_city": "Chișinău"
    },
    "Paraguay": {
        "capital_major_city": "Asunción"
    },
    "São Tomé and Príncipe": {
        "capital_major_city": "São Tomé",
        "largest_city": "São Tomé"
    },
    "Sweden": {
        "largest_city": "Stockholm"
    },
    "Switzerland": {
        "largest_city": "Zürich"
    },
    "Togo": {
        "capital_major_city": "Lomé",
        "largest_city": "Lomé"
    },
    "Tonga": {
        "capital_major_city": "Nukuʻalofa",
        "largest_city": "Nukuʻalofa"
    }
}

for pays, valeurs in corrections.items():
    for colonne, valeur in valeurs.items():
        if colonne in df_clean.columns:
            df_clean.loc[df_clean["country"] == pays, colonne] = valeur

# Vérification
print("\n===== CARACTÈRES MAL ENCODÉS RESTANTS =====")

reste = 0

for col in ["country", "capital_major_city", "largest_city"]:
    nb = df_clean[col].astype(str).str.contains("�", na=False).sum()
    print(f"{col} : {nb}")
    reste += nb

if reste == 0:
    print("\n✅ Tous les caractères mal encodés ont été corrigés.")
else:
    print(f"\n⚠️ Il reste {reste} valeur(s) à corriger.")

# ==========================================================
# 6. Vérification qu'il ne reste plus d'erreurs
# ==========================================================

print("\n===== VÉRIFICATION =====")

for col in df_clean.select_dtypes(include="object"):
    nb = df_clean[col].astype(str).str.contains("�", na=False).sum()
    print(f"{col} : {nb}")
# ==========================================================
# 5. Correction des caractères mal encodés
# ==========================================================

# Capitales corrigées selon le pays
capitales = {
    "Brazil": "Brasília",
    "Cameroon": "Yaoundé",
    "Colombia": "Bogotá",
    "Costa Rica": "San José",
    "Iceland": "Reykjavík",
    "Maldives": "Malé",
    "Moldova": "Chișinău",
    "Paraguay": "Asunción",
    "Togo": "Lomé",
    "Tonga": "Nukuʻalofa"
}

# Plus grandes villes corrigées selon le pays
grandes_villes = {
    "Brazil": "São Paulo",
    "Colombia": "Bogotá",
    "Costa Rica": "San José",
    "Cyprus": "Strovolos",
    "Iceland": "Reykjavík",
    "Maldives": "Malé",
    "Moldova": "Chișinău",
    "Switzerland": "Zürich",
    "Togo": "Lomé",
    "Tonga": "Nukuʻalofa"
}

# Pays corrigé
df_clean["country"] = df_clean["country"].replace({
    "S�����������": "São Tomé and Príncipe"
})

# Correction des capitales
for pays, capitale in capitales.items():
    df_clean.loc[df_clean["country"] == pays, "capital_major_city"] = capitale

# Correction des plus grandes villes
for pays, ville in grandes_villes.items():
    df_clean.loc[df_clean["country"] == pays, "largest_city"] = ville

# Vérification
print("\n===== CARACTÈRES MAL ENCODÉS RESTANTS =====")

for col in ["country", "capital_major_city", "largest_city"]:
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

# ==========================================================
# 11. Export du Dataframe nettoyé
# ==========================================================

# ==========================================================
# 6. Sauvegarde
# ==========================================================

output_path = BASE_DIR / "data" / "world-data-2023-clean.csv"

df_clean.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\nFichier nettoyé enregistré :", output_path)