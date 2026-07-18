# ==========================================================
# ANALYSE EXPLORATOIRE (EDA) - WORLD DATA 2023
# Problématique métier :
# Identifier les principaux indicateurs socio-économiques
# pouvant caractériser les pays les plus attractifs
# pour un investissement international.
# ==========================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================================
# CONFIGURATION
# ==========================================================

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# ==========================================================
# CHARGEMENT DU DATASET
# ==========================================================

BASE_DIR = Path.cwd()

DATA_PATH = BASE_DIR / "world-data-2023-clean.csv"

if not DATA_PATH.exists():
    DATA_PATH = BASE_DIR / "data" / "world-data-2023-clean.csv"

FIGURES_PATH = BASE_DIR / "figures"
FIGURES_PATH.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

# ==========================================================
# CONVERSION EXPLICITE DES VARIABLES NUMÉRIQUES
# ==========================================================

colonnes_numeriques = [
    "GDP",
    "Population",
    "Life_expectancy",
    "Gross_tertiary_education_enrollment_pct",
    "Physicians_per_thousand",
    "Infant_mortality",
    "Urban_population",
    "Unemployment_rate"
]

for col in colonnes_numeriques:

    if col in df.columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.replace("€", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.strip()
        )

        df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========================================================
# CRÉATION DU PIB PAR HABITANT
# ==========================================================

df["GDP_per_capita"] = df["GDP"] / df["Population"]

# ==========================================================
# VÉRIFICATION DES TYPES
# ==========================================================

print("=" * 70)
print("TYPES DES VARIABLES")
print("=" * 70)

for col in colonnes_numeriques:

    if col in df.columns:
        print(f"{col:<45} {df[col].dtype}")

# ==========================================================
# IMPUTATION DES VALEURS MANQUANTES
# ==========================================================

for col in colonnes_numeriques:

    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

# ==========================================================
# VARIABLES ÉTUDIÉES
# ==========================================================

variables = [col for col in colonnes_numeriques if col in df.columns]

# ==========================================================
# STATISTIQUES DESCRIPTIVES
# ==========================================================

print("\n" + "=" * 70)
print("STATISTIQUES DESCRIPTIVES")
print("=" * 70)

for col in variables:

    print(f"\n----- {col} -----")
    print(f"Moyenne      : {df[col].mean():,.2f}")
    print(f"Médiane      : {df[col].median():,.2f}")
    print(f"Minimum      : {df[col].min():,.2f}")
    print(f"Maximum      : {df[col].max():,.2f}")
    print(f"Écart-type   : {df[col].std():,.2f}")

# ==========================================================
# DISTRIBUTION DES VARIABLES
# ==========================================================

for col in variables:

    plt.figure(figsize=(8,5))

    sns.histplot(
        data=df,
        x=col,
        bins=20,
        kde=True
    )

    plt.title(f"Distribution de {col}")
    plt.xlabel(col)
    plt.ylabel("Nombre de pays")

    plt.tight_layout()

    plt.savefig(
        FIGURES_PATH / f"hist_{col}.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# BOXPLOTS
# ==========================================================

for col in variables:

    plt.figure(figsize=(8,3))

    sns.boxplot(x=df[col])

    plt.title(f"Valeurs aberrantes - {col}")

    plt.tight_layout()

    plt.savefig(
        FIGURES_PATH / f"boxplot_{col}.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# MATRICE DE CORRÉLATION
# ==========================================================

variables = [
    "GDP_per_capita",
    "Life_expectancy",
    "Gross_tertiary_education_enrollment_pct",
    "Physicians_per_thousand",
    "Infant_mortality",
    "Urban_population",
    "Unemployment_rate"
]

# Vérifier que les colonnes existent
variables = [col for col in variables if col in df.columns]

# Matrice de corrélation
corr = df[variables].corr()

# Création de la figure
plt.figure(figsize=(8, 6))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    fmt=".2f",
    linewidths=0.5
)

plt.title("Corrélation des principaux indicateurs socio-économiques")
plt.tight_layout()

# Enregistrer la figure AVANT de l'afficher
plt.savefig(
    FIGURES_PATH / "correlation_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================================
# VARIABLES LES PLUS CORRÉLÉES AU PIB
# ==========================================================

print("\nCorrélations avec le PIB par habitant\n")

print(
    corr["GDP_per_capita"]
    .sort_values(ascending=False)
)

print(
    corr["GDP_per_capita"]
    .sort_values(ascending=False)
)

# ==========================================================
# PIB vs ESPÉRANCE DE VIE
# ==========================================================

if {"GDP_per_capita", "Life_expectancy"}.issubset(df.columns):

  plt.figure(figsize=(8,6))

sns.regplot(
    data=df,
    x="GDP_per_capita",
    y="Life_expectancy",
    scatter_kws={"alpha":0.7}
)

# Échelle logarithmique sur l'axe des x
plt.xscale("log")

plt.xlabel("GDP_per_capita (échelle logarithmique)")
plt.ylabel("Espérance de vie (années)")
plt.title("Relation entre le PIB par habitant et l'espérance de vie")

plt.tight_layout()

plt.savefig(
    FIGURES_PATH / "gdp_life_expectancy.png",
    dpi=300
)

plt.show()

# ==========================================================
# PIB vs ÉDUCATION
# ==========================================================

if {"GDP_per_capita","Gross_tertiary_education_enrollment_pct"}.issubset(df.columns):

    plt.figure(figsize=(8,6))

    sns.regplot(
        data=df,
        x="GDP_per_capita",
        y="Gross_tertiary_education_enrollment_pct",
        scatter_kws={"alpha":0.7}
    )

    plt.xscale("log")   
    plt.title("PIB vs Enseignement supérieur")

    plt.tight_layout()

    plt.savefig(
        FIGURES_PATH / "gdp_education.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# PIB vs MÉDECINS
# ==========================================================

if {"GDP_per_capita","Physicians_per_thousand"}.issubset(df.columns):

    plt.figure(figsize=(8,6))

    sns.regplot(
        data=df,
        x="GDP_per_capita",
        y="Physicians_per_thousand",
        scatter_kws={"alpha":0.7}
    )

    plt.xscale("log")
    plt.title("PIB vs Médecins pour 1000 habitants")

    plt.tight_layout()

    plt.savefig(
        FIGURES_PATH / "gdp_physicians.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# PIB vs MORTALITÉ INFANTILE
# ==========================================================

if {"GDP_per_capita","Infant_mortality"}.issubset(df.columns):

    plt.figure(figsize=(8,6))

    sns.regplot(
        data=df,
        x="GDP_per_capita",
        y="Infant_mortality",
        scatter_kws={"alpha":0.7}
    )

    plt.xscale("log")
    plt.title("PIB vs Mortalité infantile")

    plt.tight_layout()

    plt.savefig(
        FIGURES_PATH / "gdp_infant_mortality.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# PIB vs POPULATION URBAINE
# ==========================================================

if {"GDP_per_capita","Urban_population"}.issubset(df.columns):

    plt.figure(figsize=(8,6))

    sns.regplot(
        data=df,
        x="GDP_per_capita",
        y="Urban_population",
        scatter_kws={"alpha":0.7}
    )

    plt.xscale("log")
    plt.title("PIB vs Population urbaine")

    plt.tight_layout()

    plt.savefig(
        FIGURES_PATH / "gdp_urban_population.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# PIB vs CHÔMAGE
# ==========================================================

if {"GDP_per_capita","Unemployment_rate"}.issubset(df.columns):

    plt.figure(figsize=(8,6))

    sns.regplot(
        data=df,
        x="GDP_per_capita",
        y="Unemployment_rate",
        scatter_kws={"alpha":0.7}
    )

    plt.xscale("log")
    plt.title("PIB vs Taux de chômage")

    plt.tight_layout()

    plt.savefig(
        FIGURES_PATH / "gdp_unemployment.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# TOP 10 PIB
# ==========================================================

if {"Country","GDP"}.issubset(df.columns):

    top = df.sort_values("GDP", ascending=False).head(10)

    plt.figure(figsize=(10,6))

    sns.barplot(
        data=top,
        x="GDP",
        y="Country"
    )

    plt.title("Top 10 des PIB")

    plt.tight_layout()

    plt.savefig(
        FIGURES_PATH / "top10_gdp.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# TOP 10 ESPÉRANCE DE VIE
# ==========================================================

if {"Country","Life_expectancy"}.issubset(df.columns):

    top = df.sort_values("Life_expectancy", ascending=False).head(10)

    plt.figure(figsize=(10,6))

    sns.barplot(
        data=top,
        x="Life_expectancy",
        y="Country"
    )

    plt.title("Top 10 de l'espérance de vie")

    plt.tight_layout()

    plt.savefig(
        FIGURES_PATH / "top10_life_expectancy.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# TOP 10 ÉDUCATION
# ==========================================================

if {"Country","Gross_tertiary_education_enrollment_pct"}.issubset(df.columns):

    top = df.sort_values(
        "Gross_tertiary_education_enrollment_pct",
        ascending=False
    ).head(10)

    plt.figure(figsize=(10,6))

    sns.barplot(
        data=top,
        x="Gross_tertiary_education_enrollment_pct",
        y="Country"
    )

    plt.title("Top 10 de l'enseignement supérieur")

    plt.tight_layout()

    plt.savefig(
        FIGURES_PATH / "top10_education.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# TOP 10 MÉDECINS
# ==========================================================

if {"Country","Physicians_per_thousand"}.issubset(df.columns):

    top = df.sort_values(
        "Physicians_per_thousand",
        ascending=False
    ).head(10)

    plt.figure(figsize=(10,6))

    sns.barplot(
        data=top,
        x="Physicians_per_thousand",
        y="Country"
    )

    plt.title("Top 10 des médecins pour 1000 habitants")

    plt.tight_layout()

    plt.savefig(
        FIGURES_PATH / "top10_physicians.png",
        dpi=300
    )

    plt.show()

# ==========================================================
# CONCLUSION MÉTIER
# ==========================================================

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)

print("""
L'analyse exploratoire met en évidence plusieurs indicateurs associés
aux pays susceptibles d'être attractifs pour un investissement international.

Les pays présentant un PIB élevé disposent généralement :

• d'une espérance de vie plus élevée ;
• d'un meilleur niveau d'enseignement supérieur ;
• d'une densité de médecins plus importante ;
• d'une mortalité infantile plus faible ;
• d'une urbanisation plus importante.

Ces indicateurs traduisent un niveau de développement économique et
social plus élevé et constituent des critères pertinents pour orienter
une stratégie d'investissement international.

Cette analyse reste exploratoire : elle met en évidence des associations
entre variables sans établir de relation de causalité.
""")