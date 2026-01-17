#!/usr/bin/env python3
"""
Statistical Analysis of Child Health Indicators
Cameroon Demographic and Health Survey 2018
PROPER DATA EXTRACTION FROM EXCEL FILES

Author: Gilles Momeni
Institution: ISJ
Date: January 2026
"""

import warnings
warnings.filterwarnings('default')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================

def setup_matplotlib():
    """Setup matplotlib for Chapter 10 style charts."""
    plt.switch_backend("Agg")
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"
    plt.rcParams["savefig.facecolor"] = "white"
    plt.rcParams["figure.dpi"] = 150
    plt.rcParams["savefig.dpi"] = 150

# Paths
INPUT_DIR = Path("user_input_files")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Chapter 10 Colors
COLORS = {
    'green': '#7CB342',
    'blue': '#42A5F5',
    'dark_blue': '#1976D2',
    'orange': '#FF9800',
    'red': '#D32F2F',
    'light_blue': '#81D4FA',
    'total_green': '#4CAF50'
}

# =============================================================================
# DATA EXTRACTION FROM EXCEL FILES
# =============================================================================

class DHSDataExtractor:
    """Extract data directly from DHS Excel tables."""
    
    def __init__(self, input_dir):
        self.input_dir = Path(input_dir)
        self.data = {}
        
    def load_excel_files(self):
        """Load all Excel files."""
        print("=" * 70)
        print("LOADING DATA FROM EXCEL FILES")
        print("=" * 70)
        
        # Load Diarrhea tables
        diar_file = self.input_dir / "Tables_DIAR.xls"
        print(f"\nLoading: {diar_file}")
        
        self.df_diarrhea = pd.read_excel(diar_file, sheet_name='Diarrhea')
        print(f"  - Diarrhea sheet: {len(self.df_diarrhea)} rows")
        
        self.df_ors = pd.read_excel(diar_file, sheet_name='ORS')
        print(f"  - ORS sheet: {len(self.df_ors)} rows")
        
        self.df_feeding = pd.read_excel(diar_file, sheet_name='Feeding')
        print(f"  - Feeding sheet: {len(self.df_feeding)} rows")
        
        # Load ARI/Fever tables
        ari_file = self.input_dir / "Tables_ARI_FV.xls"
        print(f"\nLoading: {ari_file}")
        
        self.df_fever = pd.read_excel(ari_file, sheet_name='Fever')
        print(f"  - Fever sheet: {len(self.df_fever)} rows")
        
        self.df_ari = pd.read_excel(ari_file, sheet_name='ARI')
        print(f"  - ARI sheet: {len(self.df_ari)} rows")
        
    def get_total_row(self, df):
        """Get the Total/Ensemble row from a dataframe."""
        mask = df['row_labels'].str.contains('Total|Ensemble', case=False, na=False)
        return df[mask].iloc[0] if mask.any() else None
    
    def extract_morbidity_indicators(self):
        """Extract key morbidity indicators from Total rows."""
        print("\n" + "=" * 70)
        print("EXTRACTING KEY INDICATORS FROM EXCEL DATA")
        print("=" * 70)
        
        # Diarrhea
        total_diar = self.get_total_row(self.df_diarrhea)
        self.data['diarrhea_prevalence'] = total_diar['Diarrhea in the 2 weeks before the survey|Yes']
        self.data['diarrhea_treatment'] = total_diar['Advice or treatment sought for diarrhea|Yes']
        print(f"\nDiarrhée (from Excel):")
        print(f"  Prévalence: {self.data['diarrhea_prevalence']:.1f}%")
        print(f"  Traitement: {self.data['diarrhea_treatment']:.1f}%")
        
        # Fever
        total_fever = self.get_total_row(self.df_fever)
        self.data['fever_prevalence'] = total_fever['Fever symptoms in the 2 weeks before the survey|Yes']
        self.data['fever_treatment'] = total_fever['Advice or treatment sought for fever symptoms|Yes']
        print(f"\nFièvre (from Excel):")
        print(f"  Prévalence: {self.data['fever_prevalence']:.1f}%")
        print(f"  Traitement: {self.data['fever_treatment']:.1f}%")
        
        # ARI
        total_ari = self.get_total_row(self.df_ari)
        self.data['ari_prevalence'] = total_ari['ARI symptoms in the 2 weeks before the survey|Yes']
        self.data['ari_treatment'] = total_ari['Advice or treatment sought for ARI symptoms|Yes']
        print(f"\nIRA (from Excel):")
        print(f"  Prévalence: {self.data['ari_prevalence']:.1f}%")
        print(f"  Traitement: {self.data['ari_treatment']:.1f}%")
        
    def extract_diarrhea_by_age(self):
        """Extract diarrhea prevalence by age group."""
        print("\n" + "-" * 50)
        print("Extracting diarrhea by age group...")
        
        age_mapping = {
            '<6': '<6',
            '6-11': '6-11',
            '12-23': '12-23',
            '24-35': '24-35',
            '36-47': '36-47',
            '48-59': '48-59'
        }
        
        age_data = []
        for age_key, age_label in age_mapping.items():
            mask = self.df_diarrhea['row_labels'].str.contains(f'|{age_key}', regex=False, na=False)
            mask &= ~self.df_diarrhea['row_labels'].str.contains('Weighted', case=False, na=False)
            
            if mask.any():
                row = self.df_diarrhea[mask].iloc[0]
                prevalence = row['Diarrhea in the 2 weeks before the survey|Yes']
                age_data.append({'age_group': age_label, 'prevalence': prevalence})
                print(f"  {age_label}: {prevalence:.1f}%")
        
        # Add Ensemble
        age_data.append({'age_group': 'Ensemble', 'prevalence': self.data['diarrhea_prevalence']})
        print(f"  Ensemble: {self.data['diarrhea_prevalence']:.1f}%")
        
        self.data['diarrhea_by_age'] = pd.DataFrame(age_data)
        
    def extract_diarrhea_treatment(self):
        """Extract diarrhea treatment indicators from ORS sheet."""
        print("\n" + "-" * 50)
        print("Extracting diarrhea treatment data...")
        
        total_ors = self.get_total_row(self.df_ors)
        
        self.data['treatment'] = {
            'Recherche conseil/traitement': self.data['diarrhea_treatment'],
            'SRO (sachet)': total_ors['Given oral rehydration salts for diarrhea|Yes'],
            'Solution maison recommandée': total_ors['Given recommended homemade fluids for diarrhea|Yes'],
            'SRO ou SMR': total_ors['Given either ORS or RHF for diarrhea|Yes'],
            'Zinc': total_ors['Given zinc for diarrhea|Yes'],
            'SRO et zinc': total_ors['Given zinc and ORS for diarrhea|Yes'],
            'SRO ou liquides augmentés': total_ors['Given ORS or increased fluids for diarrhea|Yes'],
            'TRO': total_ors['Given oral rehydration treatment or increased liquids for diarrhea|Yes'],
            'Antibiotiques': total_ors['Given antibiotic drugs for diarrhea|Yes'],
            'Remède maison/autre': total_ors['Given home remedy or other treatment for diarrhea|Yes'],
            'Aucun traitement': total_ors['No treatment for diarrhea|Yes']
        }
        
        for treatment, value in self.data['treatment'].items():
            print(f"  {treatment}: {value:.1f}%")
            
    def extract_feeding_practices(self):
        """Extract feeding practices during diarrhea."""
        print("\n" + "-" * 50)
        print("Extracting feeding practices during diarrhea...")
        
        total_feeding = self.get_total_row(self.df_feeding)
        cols = self.df_feeding.columns.tolist()
        
        # Find columns for fluids and foods
        self.data['feeding'] = {
            'Liquides donnés': {},
            'Aliments donnés': {}
        }
        
        # Extract fluid data
        for col in cols:
            if 'fluids' in col.lower():
                if 'more' in col.lower():
                    self.data['feeding']['Liquides donnés']['Davantage'] = total_feeding[col]
                elif 'same' in col.lower():
                    self.data['feeding']['Liquides donnés']['Même'] = total_feeding[col]
                elif 'less' in col.lower():
                    self.data['feeding']['Liquides donnés']['Moins'] = total_feeding[col]
                elif 'nothing' in col.lower() or 'none' in col.lower():
                    self.data['feeding']['Liquides donnés']['Rien'] = total_feeding[col]
                    
        # Extract food data  
        for col in cols:
            if 'food' in col.lower():
                if 'more' in col.lower():
                    self.data['feeding']['Aliments donnés']['Davantage'] = total_feeding[col]
                elif 'same' in col.lower():
                    self.data['feeding']['Aliments donnés']['Même'] = total_feeding[col]
                elif 'less' in col.lower():
                    self.data['feeding']['Aliments donnés']['Moins'] = total_feeding[col]
                elif 'nothing' in col.lower() or 'none' in col.lower() or 'never' in col.lower():
                    self.data['feeding']['Aliments donnés']['Rien'] = total_feeding[col]
        
        print(f"  Liquides: {self.data['feeding']['Liquides donnés']}")
        print(f"  Aliments: {self.data['feeding']['Aliments donnés']}")
        
    def run_extraction(self):
        """Run all extraction steps."""
        self.load_excel_files()
        self.extract_morbidity_indicators()
        self.extract_diarrhea_by_age()
        self.extract_diarrhea_treatment()
        self.extract_feeding_practices()
        return self.data

# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================

def graphique_10_8(data):
    """Graphique 10.8: Prévalence et traitement - Dual panel."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    conditions = ['IRA', 'Fièvre', 'Diarrhée']
    prevalence = [
        round(data['ari_prevalence']),
        round(data['fever_prevalence']),
        round(data['diarrhea_prevalence'])
    ]
    treatment = [
        round(data['ari_treatment']),
        round(data['fever_treatment']),
        round(data['diarrhea_treatment'])
    ]
    
    # Left panel - Prevalence
    bars1 = ax1.bar(conditions, prevalence, color=COLORS['green'], width=0.5)
    for bar, val in zip(bars1, prevalence):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{val}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax1.set_title('Pourcentage d\'enfants de moins de\n5 ans ayant présenté des symptômes\n'
                 'au cours des 2 semaines avant l\'interview', fontsize=10)
    ax1.set_ylim(0, max(prevalence) + 5)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.tick_params(left=False)
    ax1.set_yticks([])
    
    # Right panel - Treatment
    bars2 = ax2.bar(conditions, treatment, color=COLORS['blue'], width=0.5)
    for bar, val in zip(bars2, treatment):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{val}%', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    ax2.set_title('Parmi ces enfants malades, pourcentage\npour lesquels on a recherché\n'
                 'des conseils ou un traitement', fontsize=10)
    ax2.set_ylim(0, max(treatment) + 10)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.tick_params(left=False)
    ax2.set_yticks([])
    
    fig.suptitle('Graphique 10.8  Prévalence et traitement des maladies infantiles', 
                fontsize=12, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "graphique_10_8_prevalence_treatment.png", bbox_inches='tight')
    plt.close()
    print("  Saved: graphique_10_8_prevalence_treatment.png")

def graphique_10_6(data):
    """Graphique 10.6: Diarrhée par âge."""
    df = data['diarrhea_by_age']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = [COLORS['blue'] if age != 'Ensemble' else COLORS['total_green'] 
              for age in df['age_group']]
    
    bars = ax.bar(df['age_group'], df['prevalence'], color=colors, width=0.6)
    
    for bar, val in zip(bars, df['prevalence']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
               f'{round(val)}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.set_xlabel('Âge en mois', fontsize=11)
    ax.set_ylim(0, df['prevalence'].max() + 5)
    ax.set_title('Graphique 10.6  Prévalence de la diarrhée, par âge\n'
                'Pourcentage d\'enfants de moins de 5 ans ayant eu la diarrhée\n'
                'au cours des 2 semaines avant l\'enquête', fontsize=11, fontweight='bold', loc='left')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(left=False)
    ax.set_yticks([])
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "graphique_10_6_diarrhea_age.png", bbox_inches='tight')
    plt.close()
    print("  Saved: graphique_10_6_diarrhea_age.png")

def graphique_10_5(data):
    """Graphique 10.5: Traitement de la diarrhée."""
    treatment = data['treatment']
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    labels = list(treatment.keys())[::-1]
    values = [treatment[l] for l in labels[::-1]][::-1]
    
    # Color coding
    colors = []
    for label in labels:
        if 'Recherche' in label:
            colors.append('#D32F2F')
        elif 'SRO' in label or 'Solution' in label:
            colors.append('#FF9800')
        elif 'Zinc' in label:
            colors.append('#81D4FA')
        elif 'TRO' in label or 'liquides' in label:
            colors.append('#4CAF50')
        else:
            colors.append('#1976D2')
    
    bars = ax.barh(labels, values, color=colors, height=0.7)
    
    for bar, val in zip(bars, values):
        ax.text(val + 1, bar.get_y() + bar.get_height()/2, 
               f'{round(val)}', va='center', ha='left', fontsize=10, fontweight='bold')
    
    ax.set_xlim(0, max(values) + 10)
    ax.set_title('Graphique 10.5  Traitement de la diarrhée\n'
                'Pourcentage d\'enfants de moins de 5 ans ayant eu la diarrhée\n'
                'au cours des 2 semaines avant l\'interview', fontsize=11, fontweight='bold', loc='left')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(bottom=False)
    ax.set_xticks([])
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "graphique_10_5_diarrhea_treatment.png", bbox_inches='tight')
    plt.close()
    print("  Saved: graphique_10_5_diarrhea_treatment.png")

def graphique_10_7(data):
    """Graphique 10.7: Pratiques alimentaires."""
    fig, ax = plt.subplots(figsize=(12, 4))
    
    feeding = data['feeding']
    
    color_map = {
        'Davantage': '#7CB342',
        'Même': '#42A5F5',
        'Moins': '#FF9800',
        'Rien': '#8B0000'
    }
    
    categories = ['Liquides donnés\n(par rapport à la normale)', 
                  'Aliments donnés\n(par rapport à la normale)']
    
    # Plot liquids
    y_pos = 1
    left = 0
    for key in ['Davantage', 'Même', 'Moins', 'Rien']:
        val = feeding['Liquides donnés'].get(key, 0)
        if val and not np.isnan(val):
            ax.barh(y_pos, val, left=left, color=color_map[key], height=0.5, edgecolor='white')
            if val > 5:
                ax.text(left + val/2, y_pos, f'{round(val)}', ha='center', va='center', 
                       fontsize=10, fontweight='bold', color='white')
            left += val
    
    # Plot foods
    y_pos = 0
    left = 0
    for key in ['Davantage', 'Même', 'Moins', 'Rien']:
        val = feeding['Aliments donnés'].get(key, 0)
        if val and not np.isnan(val):
            ax.barh(y_pos, val, left=left, color=color_map[key], height=0.5, edgecolor='white')
            if val > 5:
                ax.text(left + val/2, y_pos, f'{round(val)}', ha='center', va='center', 
                       fontsize=10, fontweight='bold', color='white')
            left += val
    
    ax.set_yticks([0, 1])
    ax.set_yticklabels(categories[::-1])
    ax.set_xlim(0, 100)
    
    ax.set_title('Graphique 10.7  Pratiques alimentaires pendant la diarrhée\n'
                'Pourcentage d\'enfants de moins de 5 ans ayant eu la diarrhée\n'
                'au cours des 2 semaines avant l\'interview', fontsize=11, fontweight='bold', loc='left')
    
    # Legend
    legend_patches = [mpatches.Patch(color=color_map[k], label=k) for k in color_map]
    ax.legend(handles=legend_patches, loc='upper center', bbox_to_anchor=(0.5, -0.15),
             ncol=4, frameon=False, fontsize=9)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.tick_params(bottom=False)
    ax.set_xticks([])
    
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "graphique_10_7_feeding_practices.png", bbox_inches='tight')
    plt.close()
    print("  Saved: graphique_10_7_feeding_practices.png")

# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_report(data):
    """Generate the academic report."""
    
    report = f"""# Indicateurs de Santé de l'Enfant
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
| IRA | {data['ari_prevalence']:.1f}% | {data['ari_treatment']:.1f}% |
| Fièvre | {data['fever_prevalence']:.1f}% | {data['fever_treatment']:.1f}% |
| Diarrhée | {data['diarrhea_prevalence']:.1f}% | {data['diarrhea_treatment']:.1f}% |

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
"""
    
    for _, row in data['diarrhea_by_age'].iterrows():
        report += f"| {row['age_group']} | {row['prevalence']:.1f} |\n"
    
    report += f"""

### 2.2 Traitement de la Diarrhée

![Traitement de la diarrhée](output/graphique_10_5_diarrhea_treatment.png)

*Graphique 10.5: Types de traitement (données Excel - feuille ORS)*

**Données extraites du fichier Tables_DIAR.xls (feuille ORS):**

| Traitement | Pourcentage |
|------------|-------------|
"""
    
    for treatment, value in data['treatment'].items():
        report += f"| {treatment} | {value:.1f}% |\n"
    
    report += f"""

### 2.3 Pratiques Alimentaires

![Pratiques alimentaires](output/graphique_10_7_feeding_practices.png)

*Graphique 10.7: Pratiques alimentaires pendant la diarrhée (données Excel)*

---

## 3. Fièvre

- **Prévalence:** {data['fever_prevalence']:.1f}% des enfants de moins de 5 ans
- **Traitement recherché:** {data['fever_treatment']:.1f}%

---

## 4. Infections Respiratoires Aiguës

- **Prévalence:** {data['ari_prevalence']:.1f}% des enfants
- **Traitement recherché:** {data['ari_treatment']:.1f}%

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
"""
    
    return report

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    print()
    print("=" * 70)
    print("ANALYSE DE SANTÉ INFANTILE - CAMEROUN EDS 2018")
    print("EXTRACTION DIRECTE DES DONNÉES EXCEL")
    print("=" * 70)
    print()
    
    # Setup
    setup_matplotlib()
    
    # Extract data from Excel files
    extractor = DHSDataExtractor(INPUT_DIR)
    data = extractor.run_extraction()
    
    # Generate visualizations
    print("\n" + "=" * 70)
    print("GÉNÉRATION DES GRAPHIQUES")
    print("=" * 70)
    
    graphique_10_8(data)
    graphique_10_6(data)
    graphique_10_5(data)
    graphique_10_7(data)
    
    # Generate report
    print("\n" + "=" * 70)
    print("GÉNÉRATION DU RAPPORT")
    print("=" * 70)
    
    report = generate_report(data)
    report_path = OUTPUT_DIR / "Rapport_Sante_Infantile_Cameroun_2018.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"  Saved: {report_path}")
    
    # Summary
    print("\n" + "=" * 70)
    print("ANALYSE TERMINÉE!")
    print("=" * 70)
    print("\nDonnées extraites des fichiers Excel:")
    print(f"  - Tables_DIAR.xls (Diarrhée, ORS, Alimentation)")
    print(f"  - Tables_ARI_FV.xls (IRA, Fièvre)")
    print(f"\nFichiers de sortie: {OUTPUT_DIR}/")
    print("=" * 70)

if __name__ == "__main__":
    main()
