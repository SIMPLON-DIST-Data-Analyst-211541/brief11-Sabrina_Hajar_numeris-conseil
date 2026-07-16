# importation des bibliothèques
import pandas as pd
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

# Moyenne des variables numériques
df.mean(numeric_only=True)

# Mediane des variables numériques
df.median(numeric_only=True)

# Ecart type des variables numériques
df.std(numeric_only=True)

# Valeurs minimales et maximales des variables numériques
df.min(numeric_only=True)
df.max(numeric_only=True)

# Quartiles des variables numériques
df.quantile([0.25,0.5,0.75], numeric_only=True)

# Vérifier les valeurs manquantes
df.isnull().sum()

# Vérifier les doublons
df.duplicated().sum()

# Corrélations entre les variables numériques
df.corr(numeric_only=True)
# Cette étape sera très utile avant de réaliser une heatmap







