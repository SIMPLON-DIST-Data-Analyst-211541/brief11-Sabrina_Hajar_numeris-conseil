# COMMENTAIRE DU NOTEBOOK DE l'analyse exploratoire DU DATASET WORLD DATA 2023

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ==========================================================
# CRÉATION DES DOSSIERS DE SORTIE
# ==========================================================

# Récupération du dossier racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Dossiers de sauvegarde des différents graphiques
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

# Applique le thème graphique par défaut de Seaborn
sns.set_theme(style="whitegrid")

# Définit la taille par défaut des figures (largeur, hauteur)
plt.rcParams["figure.figsize"] = (10, 6)

# ==========================================================
# CHARGEMENT DU DATASET
# ==========================================================

# Chemin principal vers le fichier de données
DATA_PATH = BASE_DIR / "world-data-2023-clean.csv"

# Vérifie si le fichier existe, sinon utilise le dossier "data"
if not DATA_PATH.exists():
    DATA_PATH = BASE_DIR / "data" / "world-data-2023-clean.csv"

# Charge le dataset dans un DataFrame Pandas
df = pd.read_csv(DATA_PATH)

# ==========================================================
# CONVERSION DES VARIABLES NUMÉRIQUES
# ==========================================================

# Liste des colonnes à convertir en valeurs numériques
colonnes_numeriques = [
    "GDP",
    "Population",
    "Life_expectancy",
    "Gross_tertiary_education_enrollment_pct",
    "Physicians_per_thousand",
    "Infant_mortality",
    "Urban_population",
    "Unemployment_rate",
]

# Parcourt chaque colonne de la liste
for col in colonnes_numeriques:
    # Vérifie que la colonne existe dans le dataset
    if col in df.columns:
        # Supprime les caractères non numériques
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.replace("€", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.strip()
        )

        # Convertit la colonne au format numérique
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ==========================================================
# CRÉATION DU PIB PAR HABITANT
# ==========================================================

# Calcule le PIB par habitant en divisant le PIB par la population
df["GDP_per_capita"] = df["GDP"] / df["Population"]

# ==========================================================
# VÉRIFICATION DES TYPES
# ==========================================================

# Affiche un titre dans la console
print("=" * 70)
print("TYPES DES VARIABLES")
print("=" * 70)

# Vérifie le type de chaque colonne numérique
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

# Sélectionne les variables numériques présentes dans le DataFrame
variables = [col for col in colonnes_numeriques if col in df.columns]

# ==========================================================
# STATISTIQUES DESCRIPTIVES
# ==========================================================

# Affiche un en-tête dans la console
print("\n" + "=" * 70)
print("STATISTIQUES DESCRIPTIVES")
print("=" * 70)

# Parcourt chaque variable numérique
for col in variables:
    # Affiche le nom de la variable
    print(f"\n----- {col} -----")

    # Calcule et affiche les principales statistiques
    print(f"Moyenne      : {df[col].mean():,.2f}")
    print(f"Médiane      : {df[col].median():,.2f}")
    print(f"Minimum      : {df[col].min():,.2f}")
    print(f"Maximum      : {df[col].max():,.2f}")
    print(f"Écart-type   : {df[col].std():,.2f}")

# ==========================================================
# DISTRIBUTION DES VARIABLES
# ==========================================================

# Génère un histogramme pour chaque variable
for col in variables:
    # Crée une nouvelle figure
    plt.figure(figsize=(8, 5))

    # Affiche la distribution des données
    sns.histplot(data=df, x=col, bins=20, kde=True)

    # Ajoute un titre et les axes
    plt.title(f"Distribution de {col}")
    plt.xlabel(col)
    plt.ylabel("Nombre de pays")

    # Ajuste automatiquement la mise en page
    plt.tight_layout()

    # Enregistre le graphique
    plt.savefig(HIST_DIR / f"hist_{col}.png", dpi=300, bbox_inches="tight")

    # Affiche le graphique
    plt.show()

# ==========================================================
# BOXPLOTS
# ==========================================================

# Liste des variables à analyser
variables = [
    "GDP_per_capita",
    "Population",
    "Life_expectancy",
    "Unemployment_rate",
    "Birth_Rate",
    "Fertility_Rate",
    "Infant_mortality",
    "Maternal_mortality_ratio",
    "CPI_Change_pct",
]

# Affiche un aperçu des données
print(df.head())
print(df.columns)

# Vérifie les colonnes présentes dans le dataset
colonnes_existantes = [col for col in variables if col in df.columns]
colonnes_manquantes = [col for col in variables if col not in df.columns]

# Affiche les colonnes absentes si nécessaire
if colonnes_manquantes:
    print("Colonnes manquantes :", colonnes_manquantes)

# Génère les boxplots des variables disponibles
if colonnes_existantes:
    # Crée une grille de graphiques
    fig, axes = plt.subplots(3, 3, figsize=(18, 15))
    axes = axes.flatten()

    # Crée un boxplot pour chaque variable
    for i, variable in enumerate(colonnes_existantes):
        sns.boxplot(y=df[variable], ax=axes[i], color="skyblue")
        axes[i].set_title(variable)
        axes[i].set_ylabel("")

    # Supprime les graphiques inutilisés
    for j in range(len(colonnes_existantes), len(axes)):
        fig.delaxes(axes[j])

    # Ajuste la mise en page
    plt.tight_layout()

    # Enregistre la figure
    plt.savefig(
        BOXPLOTS_DIR / "boxplots_principaux_indicateurs.png",
        dpi=300,
        bbox_inches="tight",
    )

    # Affiche les boxplots
    plt.show()

# ==========================================================
# MATRICE DE CORRÉLATION
# ==========================================================

# Variables utilisées pour calculer les corrélations
variables = [
    "GDP_per_capita",
    "Life_expectancy",
    "Gross_tertiary_education_enrollment_pct",
    "Physicians_per_thousand",
    "Infant_mortality",
    "Urban_population",
    "Unemployment_rate",
]

# Conserve uniquement les colonnes présentes dans le DataFrame
variables = [col for col in variables if col in df.columns]

# Calcule la matrice de corrélation
corr = df[variables].corr()

# Crée la figure
plt.figure(figsize=(8, 6))

# Affiche la matrice de corrélation
sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    vmin=-1,
    vmax=1,
    fmt=".2f",
    linewidths=0.5,
)

# Ajoute un titre
plt.title("Corrélation des principaux indicateurs socio-économiques")

# Ajuste automatiquement la mise en page
plt.tight_layout()

# Enregistre la figure
plt.savefig(CORR_DIR / "correlation_matrix.png", dpi=300, bbox_inches="tight")

# Affiche la figure
plt.show()

# ==========================================================
# VARIABLES LES PLUS CORRÉLÉES AU PIB
# ==========================================================

# Affiche un titre dans la console
print("\nCorrélations avec le PIB par habitant\n")

# Trie les variables selon leur corrélation avec le PIB par habitant
correlations = (
    corr["GDP_per_capita"]
    .drop("GDP_per_capita")
    .sort_values(key=abs, ascending=False)
)

# Affiche les coefficients de corrélation
print(correlations)

# Affiche un titre
print("\n" + "=" * 70)
print("SYNTHÈSE MÉTIER")
print("=" * 70)

# Interprète chaque coefficient de corrélation
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

    # Affiche le résultat et son interprétation
    print(f"{variable:<45} {valeur:>6.2f}   {interpretation}")

# ==========================================================
# PIB vs ESPÉRANCE DE VIE
# ==========================================================

# Vérifie que les variables existent
if {"GDP_per_capita", "Life_expectancy"}.issubset(df.columns):
    # Crée une nouvelle figure
    plt.figure(figsize=(8, 6))

    # Affiche le nuage de points avec la droite de régression
    sns.regplot(
        data=df,
        x="GDP_per_capita",
        y="Life_expectancy",
        scatter_kws={"alpha": 0.7},
    )

    # Passe l'axe du PIB en échelle logarithmique
    plt.xscale("log")

    # Ajoute les titres des axes
    plt.xlabel("GDP_per_capita (échelle logarithmique)")
    plt.ylabel("Espérance de vie (années)")

    # Ajoute un titre
    plt.title("Relation entre le PIB par habitant et l'espérance de vie")

    # Ajuste la mise en page
    plt.tight_layout()

    # Enregistre le graphique
    plt.savefig(
        REGPLOT_DIR / "gdp_life_expectancy.png",
        dpi=300,
        bbox_inches="tight",
    )

    # Affiche le graphique
    plt.show()

# ==========================================================
# PIB vs ÉDUCATION
# ==========================================================

# Vérifie que les variables existent
if {"GDP_per_capita", "Gross_tertiary_education_enrollment_pct"}.issubset(df.columns):
    # Crée une nouvelle figure
    plt.figure(figsize=(8, 6))

    # Affiche le nuage de points avec la droite de régression
    sns.regplot(
        data=df,
        x="GDP_per_capita",
        y="Gross_tertiary_education_enrollment_pct",
        scatter_kws={"alpha": 0.7},
    )

    # Passe l'axe du PIB en échelle logarithmique
    plt.xscale("log")

    # Ajoute un titre
    plt.title("PIB vs Enseignement supérieur")

    # Ajuste la mise en page
    plt.tight_layout()

    # Enregistre le graphique
    plt.savefig(REGPLOT_DIR / "gdp_education.png", dpi=300, bbox_inches="tight")

    # Affiche le graphique
    plt.show()

# ==========================================================
# PIB vs MÉDECINS
# ==========================================================

# Vérifie que les variables existent
if {"GDP_per_capita", "Physicians_per_thousand"}.issubset(df.columns):
    # Crée une nouvelle figure
    plt.figure(figsize=(8, 6))

    # Affiche le nuage de points et la droite de régression
    sns.regplot(
        data=df,
        x="GDP_per_capita",
        y="Physicians_per_thousand",
        scatter_kws={"alpha": 0.7},
    )

    # Passe l'axe du PIB en échelle logarithmique
    plt.xscale("log")

    # Ajoute un titre
    plt.title("PIB vs Médecins pour 1000 habitants")

    # Ajuste la mise en page
    plt.tight_layout()

    # Enregistre le graphique
    plt.savefig(
        REGPLOT_DIR / "gdp_physicians.png",
        dpi=300,
        bbox_inches="tight",
    )

    # Affiche le graphique
    plt.show()

# ==========================================================
# PIB vs MORTALITÉ INFANTILE
# ==========================================================

# Vérifie que les variables existent
if {"GDP_per_capita", "Infant_mortality"}.issubset(df.columns):
    # Crée une nouvelle figure
    plt.figure(figsize=(8, 6))

    # Affiche le nuage de points et la droite de régression
    sns.regplot(
        data=df,
        x="GDP_per_capita",
        y="Infant_mortality",
        scatter_kws={"alpha": 0.7},
    )

    # Passe l'axe du PIB en échelle logarithmique
    plt.xscale("log")

    # Ajoute un titre
    plt.title("PIB vs Mortalité infantile")

    # Ajuste la mise en page
    plt.tight_layout()

    # Enregistre le graphique
    plt.savefig(
        REGPLOT_DIR / "gdp_infant_mortality.png",
        dpi=300,
        bbox_inches="tight",
    )

    # Affiche le graphique
    plt.show()

# ==========================================================
# PIB vs POPULATION URBAINE
# ==========================================================

# Vérifie que les variables existent
if {"GDP_per_capita", "Urban_population"}.issubset(df.columns):
    # Crée une nouvelle figure
    plt.figure(figsize=(8, 6))

    # Affiche le nuage de points et la droite de régression
    sns.regplot(
        data=df,
        x="GDP_per_capita",
        y="Urban_population",
        scatter_kws={"alpha": 0.7},
    )

    # Passe l'axe du PIB en échelle logarithmique
    plt.xscale("log")

    # Ajoute un titre
    plt.title("PIB vs Population urbaine")

    # Ajuste la mise en page
    plt.tight_layout()

    # Enregistre le graphique
    plt.savefig(
        REGPLOT_DIR / "gdp_urban_population.png",
        dpi=300,
        bbox_inches="tight",
    )

    # Affiche le graphique
    plt.show()

# ==========================================================
# PIB vs CHÔMAGE
# ==========================================================

# Vérifie que les variables existent
if {"GDP_per_capita", "Unemployment_rate"}.issubset(df.columns):
    # Crée une nouvelle figure
    plt.figure(figsize=(8, 6))

    # Affiche le nuage de points et la droite de régression
    sns.regplot(
        data=df,
        x="GDP_per_capita",
        y="Unemployment_rate",
        scatter_kws={"alpha": 0.7},
    )

    # Passe l'axe du PIB en échelle logarithmique
    plt.xscale("log")

    # Ajoute un titre
    plt.title("PIB vs Taux de chômage")

    # Ajuste la mise en page
    plt.tight_layout()

    # Enregistre le graphique
    plt.savefig(
        REGPLOT_DIR / "gdp_unemployment.png",
        dpi=300,
        bbox_inches="tight",
    )

    # Affiche le graphique
    plt.show()

# ==========================================================
# TOP 10 PIB
# ==========================================================

# Vérifie que les colonnes existent
if {"Country", "GDP"}.issubset(df.columns):
    # Sélectionne les 10 pays ayant le PIB le plus élevé
    top = df.sort_values("GDP", ascending=False).head(10)

    # Crée un graphique en barres
    plt.figure(figsize=(10, 6))

    sns.barplot(data=top, x="GDP", y="Country")

    # Ajoute un titre
    plt.title("Top 10 des PIB")

    # Ajuste la mise en page
    plt.tight_layout()

    # Enregistre le graphique
    plt.savefig(TOP10_DIR / "top10_gdp.png", dpi=300, bbox_inches="tight")

    # Affiche le graphique
    plt.show()

# ==========================================================
# INDICATEURS CLÉS POUR L'ATTRACTIVITÉ D'UN PAYS
# ==========================================================

# Classe les variables selon leur corrélation avec le PIB par habitant
top = (
    corr["GDP_per_capita"]
    .drop("GDP_per_capita")
    .abs()
    .sort_values(ascending=False)
)

# Affiche les variables les plus corrélées
for variable in top.index:
    print(f"• {variable} ({corr.loc[variable, 'GDP_per_capita']:.2f})")

# ==========================================================
# CONCLUSION MÉTIER
# ==========================================================

# Affiche une synthèse des principaux résultats
print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)

print("""
...
""")