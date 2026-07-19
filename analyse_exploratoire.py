# ==========================================================
# ANALYSE EXPLORATOIRE (EDA) - WORLD DATA 2023
# Problématique métier :
# Identifier les principaux indicateurs socio-économiques
# pouvant caractériser les pays les plus attractifs
# pour un investissement international.
# ==========================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ==========================================================
# CREATION DES DOSSIERS DE SORTIE
# ==========================================================

# Dossier du projet (le parent de notebooks)
BASE_DIR = Path(__file__).resolve().parent.parent

# Dossiers des figures
BOXPLOTS_DIR = BASE_DIR / "figures" / "boxplots"
HIST_DIR = BASE_DIR / "figures" / "histogrammes"
CORR_DIR = BASE_DIR / "figures" / "correlations"
TOP10_DIR = BASE_DIR / "figures" / "top10"
REGPLOT_DIR = BASE_DIR / "figures" / "relations"

# Création des dossiers s'ils n'existent pas
for dossier in [BOXPLOTS_DIR, HIST_DIR, CORR_DIR, TOP10_DIR, REGPLOT_DIR]:
    dossier.mkdir(parents=True, exist_ok=True)

# ==========================================================
# CONFIGURATION
# ==========================================================

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# ==========================================================
# CHARGEMENT DU DATASET
# ==========================================================

DATA_PATH = BASE_DIR / "world-data-2023-clean.csv"

if not DATA_PATH.exists():
    DATA_PATH = BASE_DIR / "data" / "world-data-2023-clean.csv"

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

    plt.savefig(HIST_DIR / f"hist_{col}.png",
            dpi=300,
            bbox_inches="tight")

    plt.show()

# ==========================================================
# BOXPLOTS
# ==========================================================

variables = [
    "GDP_per_capita",
    "Population",
    "Life_expectancy",
    "Unemployment_rate",
    "Birth_Rate",
    "Fertility_Rate",
    "Infant_mortality",
    "Maternal_mortality_ratio",
    "CPI_Change_pct"
]

print(df.head())
print(df.columns)

# Vérifier que toutes les colonnes existent
colonnes_existantes = [col for col in variables if col in df.columns]
colonnes_manquantes = [col for col in variables if col not in df.columns]

if colonnes_manquantes:
    print("Colonnes manquantes :", colonnes_manquantes)

if colonnes_existantes:
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    axes = axes.flatten()

    for i, variable in enumerate(colonnes_existantes):
        sns.boxplot(y=df[variable], ax=axes[i], color="skyblue")
        axes[i].set_title(variable)
        axes[i].set_ylabel("")

    # Supprimer les axes inutilisés si certaines colonnes manquent
    for j in range(len(colonnes_existantes), len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.savefig(BOXPLOTS_DIR / "boxplots_principaux_indicateurs.png",
            dpi=300, bbox_inches="tight")
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
    CORR_DIR / "correlation_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# ==========================================================
# VARIABLES LES PLUS CORRÉLÉES AU PIB
# ==========================================================

print("\nCorrélations avec le PIB par habitant\n")

correlations = (
    corr["GDP_per_capita"]
    .drop("GDP_per_capita")      # On retire le PIB corrélé avec lui-même (=1)
    .sort_values(key=abs, ascending=False)
)

print(correlations)

print("\n" + "=" * 70)
print("SYNTHÈSE MÉTIER")
print("=" * 70)

for variable, valeur in correlations.items():

    if valeur >= 0.70:
        interpretation = "Très forte corrélation positive"

    elif valeur >= 0.40:
        interpretation = "Corrélation positive"

    elif valeur <= -0.70:
        interpretation = "Très forte corrélation négative"

    elif valeur <= -0.40:
        interpretation = "Corrélation négative"

    else:
        interpretation = "Corrélation faible"

    print(f"{variable:<45} {valeur:>6.2f}   {interpretation}")
    
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
    REGPLOT_DIR / "gdp_life_expectancy.png",
    dpi=300,
    bbox_inches="tight"
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
        REGPLOT_DIR / "gdp_education.png",
        dpi=300,
        bbox_inches="tight"
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
        REGPLOT_DIR / "gdp_physicians.png",
        dpi=300,
        bbox_inches="tight"
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
        REGPLOT_DIR / "gdp_infant_mortality.png",
        dpi=300,
        bbox_inches="tight"
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
        REGPLOT_DIR / "gdp_urban_population.png",
        dpi=300,
        bbox_inches="tight"
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
        REGPLOT_DIR / "gdp_unemployment.png",
        dpi=300,
        bbox_inches="tight"
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
    TOP10_DIR / "top10_gdp.png",
    dpi=300,
    bbox_inches="tight"
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
        TOP10_DIR / "top10_life_expectancy.png",
        dpi=300,
        bbox_inches="tight"
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
        TOP10_DIR / "top10_education.png",
        dpi=300,
        bbox_inches="tight"
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
        TOP10_DIR / "top10_physicians.png",
        bbox_inches="tight",
        dpi=300
    )

    plt.show()

print("\nINDICATEURS CLÉS POUR L'ATTRACTIVITÉ D'UN PAYS\n")

top = (
    corr["GDP_per_capita"]
    .drop("GDP_per_capita")
    .abs()
    .sort_values(ascending=False)
)

for variable in top.index:
    print(f"• {variable} ({corr.loc[variable,'GDP_per_capita']:.2f})")

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