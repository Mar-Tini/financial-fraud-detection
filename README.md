# Détection de la fraude financière

## 1. Présentation du projet

Ce projet consiste à analyser des transactions financières et à détecter les opérations frauduleuses à l'aide du Machine Learning.

L'objectif est d'identifier les transactions frauduleuses à partir de plusieurs informations, comme le montant, le type de transaction et les soldes des comptes avant et après chaque opération.

Le jeu de données contient **6 362 620 transactions** et **11 variables**.

Chaque ligne représente une transaction financière entre un compte d'origine et, selon le type d'opération, un compte de destination.

La principale question étudiée est :

> **Quelles caractéristiques permettent d'identifier une transaction financière frauduleuse ?**

## 2. Présentation du jeu de données

Deux modèles de classification ont été utilisés : la régression logistique et Random Forest (Forêt aléatoire).

Les données ont été réparties en trois ensembles :

| Ensemble      | Nombre de transactions |
| ------------- | ---------------------: |
| Entraînement |              6 082 007 |
| Validation    |                191 147 |
| Test          |                 89 466 |

**Nombre de variables utilisées : 14**

Les variables utilisées sont :

- **Informations sur les transactions :** `step`, `amount`.
- **Soldes des comptes :** `oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, `newbalanceDest`.
- **Types de transactions :** `type_CASH_OUT`, `type_DEBIT`, `type_PAYMENT`, `type_TRANSFER`.
- **Variables calculées :** `balance_change_orig`, `balance_error_orig`, `balance_change_dest`, `balance_error_dest`.

## 3. Résultats des modèles

### 	3.1. Régression logistique (modèle de référence)

La régression logistique a été utilisée comme premier modèle pour avoir une référence et comparer ses résultats avec ceux de Random Forest.

**Résultats obtenus :**

- Accuracy : 99,87 %

| Classe                    | Précision | Rappel | F1-score |
| ------------------------- | ---------: | -----: | -------: |
| Transactions légitimes   |       1,00 |   1,00 |     1,00 |
| Transactions frauduleuses |       0,84 |   0,70 |     0,76 |

**Matrice de confusion :**

| Réalité / Prédiction | Non frauduleuse | Frauduleuse |
| ----------------------- | --------------: | ----------: |
| Non frauduleuse         |         127 088 |          18 |
| Frauduleuse             |             583 |          64 |

**Interprétation :**

La régression logistique détecte correctement la majorité des transactions légitimes. Cependant, elle identifie seulement 70 % des transactions frauduleuses.

Sur les 647 fraudes présentes dans cet ensemble, elle en détecte 64 et en manque 583.

### 	3.2. Random Forest (Forêt aléatoire)

Le modèle Random Forest a ensuite été entraîné pour améliorer la détection des transactions frauduleuses.

Les résultats ont été obtenus sur le jeu de validation avec un seuil de classification de **0,50**.

**Résultats obtenus :**

| Indicateur          |  Résultat |
| ------------------- | ---------: |
| Accuracy            | 99,99895 % |
| Précision (Fraude) |    99,83 % |
| Rappel (Fraude)     |   100,00 % |
| F1-score (Fraude)   |    99,92 % |

**Matrice de confusion :**

| Réalité / Prédiction | Non frauduleuse | Frauduleuse |
| ----------------------- | --------------: | ----------: |
| Non frauduleuse         |         189 965 |           2 |
| Frauduleuse             |               0 |       1 180 |

**Interprétation :**

Random Forest a obtenu de très bons résultats sur les données de validation.

Il a détecté les **1 180 transactions frauduleuses**, sans manquer aucune fraude. Il a également classé correctement 189 965 transactions légitimes, avec seulement 2 fausses alertes.

### 4. Conclusion

La comparaison montre que Random Forest obtient de meilleurs résultats que la régression logistique pour détecter les fraudes.

La régression logistique détecte 70 % des fraudes, tandis que Random Forest atteint 100 % sur le jeu de validation.

Random Forest est donc le meilleur modèle parmi les deux modèles testés.

Ces résultats restent à confirmer avec une évaluation finale sur le jeu de test pour vérifier les performances du modèle sur de nouvelles transactions.
