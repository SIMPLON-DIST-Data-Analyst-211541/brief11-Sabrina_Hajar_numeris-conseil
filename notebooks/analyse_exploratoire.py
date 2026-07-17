# ANALYSE EXPLORATOIRE DES DONNEES (EDA)

# Les Statistiques descriptives sont des mesures qui permettent de résumer et 
# de décrire les caractéristiques

# importation des bibliothèques
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement du dataset nettoyé
df = pd.read_csv("data/world-data-2023-clean.csv")

# Statistiques descriptives
# Nombre de lignes et de colonnes
df.shape

# Informations sur les colonnes
df.info()

# Statistiques descriptives
df.describe()

# variables de type texte
df.describe(include=["object"])

# Résumé statistique des principales variables

resume = pd.DataFrame({
    "Valeurs non nulles": df.count(numeric_only=True),
    "Valeurs manquantes": df.isnull().sum(numeric_only=True),
    "Moyenne": df.mean(numeric_only=True),
    "Médiane": df.median(numeric_only=True),
    "Écart-type": df.std(numeric_only=True),
    "Minimum": df.min(numeric_only=True),
    "Q1 (25%)": df.quantile(0.25, numeric_only=True),
    "Q3 (75%)": df.quantile(0.75, numeric_only=True),
    "Maximum": df.max(numeric_only=True)
})

resume

# Vérifier les valeurs manquantes
df.isnull().sum()

# Vérifier les doublons
df.duplicated().sum()

# Corrélations entre les variables numériques
df.corr(numeric_only=True)
# Cette étape sera très utile avant de réaliser une heatmap

# Analyse exloratoire des données (EDA)

# Corrélations entre les variables
# Objectif : identifier les relations entre les indicateurs économiques et sociaux.

corr = df.corr(numeric_only=True)
corr

# Le Heatmap est une représentation graphique des corrélations entre les variables.
# Elles permettent de visualiser rapidement les relations entre les variables 
# et d'identifier les variables qui sont fortement corrélées entre elles.

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(15,10))
sns.heatmap(corr, cmap="coolwarm", annot=False)
plt.title("Matrice de corrélation")
plt.show()

# Distribution des principales variables (PIB, Population, Taux de natalité, Indice de fécondité, 
# Mortalité infantile, Taux de mortalité maternelle, Espérance de vie, Taux de chomage, IPC, 
# Variation de l'IPC (%), Taux de natalité, Taux brut de scolarisation dans le primaire (%), 
# Taux brut de scolarisation dans le supérieur (%)).

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement du jeu de données
df = pd.read_csv("data/world-data-2023-clean.csv")

# Variables numériques à représenter
variables = [
    "GDP",
    "Population",
    "Life expectancy",
    "Unemployment rate",
    "Birth rate",
    "Fertility rate",
    "Infant mortality",
    "Maternal mortality ratio",
    "CPI Change (%)"
]

# Histogrammes
for variable in variables:

    # Vérifie que la colonne existe
    if variable not in df.columns:
        print(f"Colonne introuvable : {variable}")
        continue

    plt.figure(figsize=(8, 5))

    sns.histplot(
        data=df,
        x=variable,
        bins=30,
        kde=True
    )

    plt.title(f"Distribution de {variable}")
    plt.xlabel(variable)
    plt.ylabel("Nombre de pays")

    plt.tight_layout()
    plt.show()

# Boxplots
# Les boxplots sont des graphiques qui permettent de visualiser la distribution d'une variable.

import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Colonnes à analyser
variables_box = [
    "GDP",
    "Population",
    "Life expectancy",
    "Unemployment rate",
    "CPI Change (%)",
    "Infant mortality",
    "Maternal mortality ratio",
    "Gross tertiary education enrollment (%)"
]

# Conversion des colonnes en numérique
for col in variables_box:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Calcul automatique de la grille
n = len(variables_box)
ncols = 2
nrows = math.ceil(n / ncols)

plt.figure(figsize=(12, 4 * nrows))

# Création des boxplots
for i, variable in enumerate(variables_box, 1):
    plt.subplot(nrows, ncols, i)
    sns.boxplot(y=df[variable].dropna())
    plt.title(variable)

plt.tight_layout()
plt.show()

# Analyse des relations entre les variables
# PIB et Espérance de vie

plt.figure(figsize=(8,6))

sns.scatterplot(
    data=df,
    x="GDP",
    y="Life expectancy"
)

plt.title("Relation entre le PIB et l'espérance de vie")
plt.xlabel("PIB")
plt.ylabel("Espérance de vie")

plt.show()

# PIB et Taux de chomâge



