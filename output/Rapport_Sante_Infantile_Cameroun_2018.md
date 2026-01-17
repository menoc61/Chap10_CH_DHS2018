# Indicateurs de Santé de l'Enfant
## Analyse du Poids à la Naissance et de la Morbidité au Cameroun

### Enquête Démographique et de Santé du Cameroun 2018

---

**Auteur:** Gilles Momeni  
**Institution:** ISJ  
**Date:** Janvier 2026  
**Source des données:** Fichiers Excel EDS 2018 (Tables_DIAR.xls, Tables_ARI_FV.xls)

---

## Résumé Exécutif

Ce rapport présente une analyse statistique des indicateurs de santé infantile au Cameroun, avec **extraction directe des données des fichiers Excel fournis**.

**Résultats Clés (Extraits des fichiers Excel):**

| Indicateur | Prévalence | Traitement recherché |
|------------|------------|---------------------|
| IRA | 1.0% | 59.2% |
| Fièvre | 15.4% | 61.0% |
| Diarrhée | 11.9% | 51.6% |

---

## 1. Introduction

Cette analyse utilise les données extraites directement des tableaux Excel de l'EDS Cameroun 2018:
- `Tables_DIAR.xls` (Diarrhée, ORS, Alimentation)
- `Tables_ARI_FV.xls` (IRA, Fièvre)

---

## 2. Maladies Diarrhéiques

### 2.1 Prévalence par Âge

![Prévalence de la diarrhée par âge](output/graphique_10_6_diarrhea_age.png)

*Graphique 10.6: Prévalence de la diarrhée selon l'âge (données Excel)*

**Données extraites du fichier Tables_DIAR.xls:**

| Âge (mois) | Prévalence (%) |
|------------|----------------|
| <6 | 5.0 |
| 6-11 | 20.4 |
| 12-23 | 21.1 |
| 24-35 | 13.4 |
| 36-47 | 7.7 |
| 48-59 | 4.9 |
| Ensemble | 11.9 |


### 2.2 Traitement de la Diarrhée

![Traitement de la diarrhée](output/graphique_10_5_diarrhea_treatment.png)

*Graphique 10.5: Types de traitement (données Excel - feuille ORS)*

**Données extraites du fichier Tables_DIAR.xls (feuille ORS):**

| Traitement | Pourcentage |
|------------|-------------|
| Recherche conseil/traitement | 51.6% |
| SRO (sachet) | 17.9% |
| Solution maison recommandée | 11.1% |
| SRO ou SMR | 22.6% |
| Zinc | 20.6% |
| SRO et zinc | 7.7% |
| SRO ou liquides augmentés | 42.0% |
| TRO | 44.6% |
| Antibiotiques | 21.1% |
| Remède maison/autre | 25.4% |
| Aucun traitement | 23.4% |


### 2.3 Pratiques Alimentaires

![Pratiques alimentaires](output/graphique_10_7_feeding_practices.png)

*Graphique 10.7: Pratiques alimentaires pendant la diarrhée (données Excel)*

---

## 3. Fièvre

- **Prévalence:** 15.4% des enfants de moins de 5 ans
- **Traitement recherché:** 61.0%

---

## 4. Infections Respiratoires Aiguës

- **Prévalence:** 1.0% des enfants
- **Traitement recherché:** 59.2%

---

## 5. Prévalence et Traitement (Vue d'Ensemble)

![Prévalence et traitement](output/graphique_10_8_prevalence_treatment.png)

*Graphique 10.8: Prévalence et traitement des maladies infantiles*

---

## Références

1. Institut National de la Statistique (INS). *Enquête Démographique et de Santé du Cameroun 2018*.
2. Fichiers de données: Tables_DIAR.xls, Tables_ARI_FV.xls

---

*Rapport généré avec Python - Données extraites directement des fichiers Excel EDS 2018*
