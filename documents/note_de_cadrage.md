# Note de cadrage

## 1. Présentation de la mission

Dans le cadre du Brief 11 de Numeris Conseil, notre équipe doit réaliser un diagnostic des données avant une future modélisation prédictive.

## 2. Client fictif

Global Invest Consulting

## 3. Secteur

Conseil en investissement international.

## 4. Dataset

Nom : Countries of the World 2023

Source : Kaggle

## 5. Problématique métier

Quels sont les principaux indicateurs socio-économiques permettant d'identifier les pays les plus attractifs pour un investissement international ?

## 6. Objectifs

- Diagnostiquer la qualité des données
- Nettoyer le dataset
- Réaliser une analyse exploratoire
- Préparer une base SQL exploitable
- Préparer les données pour un futur modèle Machine Learning

## 7. Pourquoi ce dataset ?

Le dataset contient des informations démographiques, économiques, sanitaires et environnementales concernant plus de 190 pays.

Il permet d'étudier plusieurs indicateurs influençant l'attractivité économique d'un pays.

Question d'analyse
En quoi ce dataset et cette problématique sont-ils pertinents et réalistes pour une mission de diagnostic pré-ML ?

Le dataset Countries of the World 2023 est pertinent pour une mission de diagnostic pré-ML car il regroupe de nombreux indicateurs démographiques, économiques, sanitaires et environnementaux concernant près de 200 pays. Cette diversité de variables permet d'étudier les relations entre plusieurs facteurs susceptibles d'influencer l'attractivité d'un pays pour un investissement international.

La problématique choisie, « Quels sont les principaux indicateurs socio-économiques permettant d'identifier les pays les plus attractifs pour un investissement international ? », est réaliste, car de nombreux cabinets de conseil accompagnent des entreprises dans leurs décisions d'implantation à l'étranger. Avant de développer un modèle prédictif, il est indispensable d'évaluer la qualité des données, d'identifier les anomalies et de préparer un jeu de données fiable. Cette étape correspond précisément à un diagnostic pré-ML.

Le dataset est également adapté à ce type de mission puisqu'il nécessite un véritable travail de préparation : présence de valeurs manquantes, colonnes numériques stockées sous forme de texte, caractères spéciaux (symbole $, virgules, %), et homogénéisation des noms de colonnes. Ces traitements sont représentatifs des tâches réalisées par un data analyst avant toute modélisation.

Qu'est-ce qui aurait pu justifier d'écarter ce dataset ?

Ce dataset aurait pu être écarté dans plusieurs situations :

si le nombre de valeurs manquantes avait été trop important sur les variables essentielles, rendant les analyses peu fiables ;
si les informations étaient trop anciennes ou ne reflétaient plus la situation actuelle des pays ;
si les indicateurs disponibles n'étaient pas en lien avec la problématique métier retenue ;
si le volume de données avait été insuffisant ou, au contraire, si les données avaient été déjà parfaitement nettoyées, limitant l'intérêt pédagogique de la mission.

Dans notre cas, malgré la présence de valeurs manquantes et de données à nettoyer, le dataset reste suffisamment riche et exploitable pour réaliser un diagnostic data complet et préparer les données en vue d'une future modélisation Machine Learning.