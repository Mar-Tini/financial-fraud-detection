# Détection de la fraude financière

Ce projet analyse les transactions financières et construit des modèles de Machine Learning pour détecter les opérations frauduleuses.

---

## 1. Situation

Une entreprise financière traite des millions de transactions. Parmi elles, certaines sont frauduleuses et peuvent entraîner des pertes financières.

Nous disposons d'un jeu de données contenant **6 362 620 transactions** et **11 variables**.

Chaque transaction contient plusieurs informations :

- le type de transaction
- le montant
- le solde du compte avant et après l'opération
- les informations sur le compte d'origine et le compte de destination
- le statut de la transaction (frauduleuse ou légitime).

Le problème : il est difficile d'identifier automatiquement les transactions frauduleuses parmi un très grand nombre de transactions légitimes.

---

## 2. Tâche

Mon travail avait deux buts :

1. **Comprendre** les caractéristiques des transactions frauduleuses.
2. **Prédire** si une nouvelle transaction est frauduleuse ou légitime à l'aide d'un modèle de classification.

Pour savoir si les modèles sont performants, je mesure leurs résultats avec quatre indicateurs : **Accuracy, Precision, Recall et F1-score**.

---

## 3. Action

Voici ce que j'ai fait, étape par étape.

### a) Explorer les données (EDA)

- J'examine la structure du jeu de données et les types de variables.
- J'analyse la répartition des transactions selon leur type.
- J'étudie les montants des transactions.
- Je compare les transactions frauduleuses et légitimes.
- J'analyse les soldes des comptes avant et après chaque opération.
- J'identifie le déséquilibre entre les deux classes.

### b) Préparer les données

- Je transforme les variables catégorielles en variables numériques (encodage).
- Je crée de nouvelles variables à partir des changements de soldes.
- Je prépare les variables utilisées pour l'entraînement.
- Je répartis les données en trois ensembles : entraînement, validation et test.

Les données ont été réparties comme suit :

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

### c) Entraîner plusieurs modèles

J'ai testé deux modèles de classification :

- **Régression logistique :** utilisée comme modèle de référence.
- **Random Forest (Forêt aléatoire) :** utilisée pour améliorer la détection des transactions frauduleuses.

### d) Prédire et vérifier

- Je prédis si chaque transaction est frauduleuse ou légitime.
- Je compare les prédictions avec les valeurs réelles.
- Je mesure les performances avec Accuracy, Precision, Recall et F1-score.
- J'utilise une matrice de confusion pour observer les fraudes détectées, les fraudes manquées et les fausses alertes.

---

## 4. Résultat

### 4.1. Régression logistique (modèle de référence)

**Résultats obtenus :**

- Accuracy : **99,87 %**

| Mesure    | Transactions légitimes | Transactions frauduleuses |
| --------- | ----------------------: | ------------------------: |
| Precision |                    1,00 |                      0,84 |
| Recall    |                    1,00 |                      0,70 |
| F1-score  |                    1,00 |                      0,76 |

**Matrice de confusion :**

| Réalité / Prédiction | Non frauduleuse | Frauduleuse |
| ----------------------- | --------------: | ----------: |
| Non frauduleuse         |         127 088 |          18 |
| Frauduleuse             |             583 |          64 |

**Interprétation :**

La régression logistique classe correctement la majorité des transactions légitimes.

Cependant, elle détecte seulement **70 % des fraudes**. Sur les 647 transactions frauduleuses, elle en détecte 64 et en manque 583.

Cela montre que ce modèle a encore des difficultés à identifier les transactions frauduleuses.

### 4.2. Random Forest (Forêt aléatoire)

Les résultats suivants ont été obtenus sur le jeu de validation avec un seuil de classification de **0,50**.

**Résultats obtenus :**

| Mesure             |     Valeur |
| ------------------ | ---------: |
| Accuracy           | 99,99895 % |
| Precision (Fraude) |    99,83 % |
| Recall (Fraude)    |   100,00 % |
| F1-score (Fraude)  |    99,92 % |

**Matrice de confusion :**

| Réalité / Prédiction | Non frauduleuse | Frauduleuse |
| ----------------------- | --------------: | ----------: |
| Non frauduleuse         |         189 965 |           2 |
| Frauduleuse             |               0 |       1 180 |

**Interprétation :**

Random Forest obtient de très bons résultats sur le jeu de validation.

Il détecte les **1 180 transactions frauduleuses**, sans en manquer aucune. Il classe également correctement 189 965 transactions légitimes, avec seulement 2 fausses alertes.

Le modèle améliore donc fortement la détection des fraudes par rapport à la régression logistique.

### Conclusion

La comparaison montre que Random Forest obtient de meilleurs résultats que la régression logistique pour détecter les transactions frauduleuses.

La régression logistique détecte 70 % des fraudes, tandis que Random Forest atteint un rappel de 100 % sur le jeu de validation.

**Random Forest est donc le meilleur modèle parmi les deux modèles testés.**

Ces résultats restent à confirmer avec une évaluation finale sur le jeu de test pour vérifier les performances du modèle sur de nouvelles transactions.
