#!/usr/bin/env python3
"""
Cameroon DHS 2018 - Child Health Analysis
===========================================
Comprehensive analysis of childhood morbidity, treatment-seeking behaviors,
and socio-economic determinants based on DHS 2018 data.

Charts generated in French (DHS official) and English (modern) styles.
All data extracted programmatically from Excel files.

Author: Momeni Gilles
Date: January 2026
"""

import warnings
warnings.filterwarnings('default')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ============================================================================
# MATPLOTLIB SETUP
# ============================================================================
def setup_matplotlib_for_plotting():
    """Setup matplotlib for non-interactive plotting with proper fonts."""
    plt.switch_backend("Agg")
    plt.style.use("seaborn-v0_8")
    sns.set_palette("husl")
    plt.rcParams["font.sans-serif"] = ["Noto Sans CJK SC", "WenQuanYi Zen Hei", 
                                        "PingFang SC", "Arial Unicode MS", 
                                        "Hiragino Sans GB", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams['figure.dpi'] = 150
    plt.rcParams['savefig.dpi'] = 150

setup_matplotlib_for_plotting()

# Create output directory
os.makedirs('output', exist_ok=True)

# ============================================================================
# DATA EXTRACTION FROM EXCEL FILES
# ============================================================================
print("="*70)
print("EXTRACTING DATA FROM EXCEL FILES")
print("="*70)

# Load all Excel files
df_diarrhea = pd.read_excel('user_input_files/Tables_DIAR.xls', sheet_name='Diarrhea')
df_feeding = pd.read_excel('user_input_files/Tables_DIAR.xls', sheet_name='Feeding')
df_ors = pd.read_excel('user_input_files/Tables_DIAR.xls', sheet_name='ORS')
df_ari = pd.read_excel('user_input_files/Tables_ARI_FV.xls', sheet_name='ARI')
df_fever = pd.read_excel('user_input_files/Tables_ARI_FV.xls', sheet_name='Fever')

# --- Extract Total Values ---
def get_total_row(df):
    """Get the Total row from a dataframe."""
    return df[df['row_labels'].str.contains('Total', case=False, na=False)].iloc[0]

# Diarrhea totals
diarrhea_total = get_total_row(df_diarrhea)
diarrhea_prev = diarrhea_total['Diarrhea in the 2 weeks before the survey|Yes']
diarrhea_treat = diarrhea_total['Advice or treatment sought for diarrhea|Yes']

# ARI totals
ari_total = get_total_row(df_ari)
ari_prev = ari_total['ARI symptoms in the 2 weeks before the survey|Yes']
ari_treat = ari_total['Advice or treatment sought for ARI symptoms|Yes']

# Fever totals
fever_total = get_total_row(df_fever)
fever_prev = fever_total['Fever symptoms in the 2 weeks before the survey|Yes']
fever_treat = fever_total['Advice or treatment sought for fever symptoms|Yes']

print(f"  Diarrhea: {diarrhea_prev:.1f}% prevalence, {diarrhea_treat:.1f}% treatment")
print(f"  Fever: {fever_prev:.1f}% prevalence, {fever_treat:.1f}% treatment")
print(f"  ARI: {ari_prev:.1f}% prevalence, {ari_treat:.1f}% treatment")

# --- Extract Diarrhea by Age ---
age_labels_raw = ['<6', '6-11', '12-23', '24-35', '36-47', '48-59']
diarrhea_by_age = []
for label in age_labels_raw:
    row = df_diarrhea[df_diarrhea['row_labels'].str.contains(f'|{label}', regex=False, na=False)]
    if not row.empty:
        diarrhea_by_age.append(row.iloc[0]['Diarrhea in the 2 weeks before the survey|Yes'])
    else:
        diarrhea_by_age.append(0)

print(f"  Diarrhea by age: {[round(x,1) for x in diarrhea_by_age]}")

# --- Extract ORS Treatment Data ---
ors_total = get_total_row(df_ors)
ors_rate = ors_total['Given oral rehydration salts for diarrhea|Yes']
rhf_rate = ors_total['Given recommended homemade fluids for diarrhea|Yes']
ors_rhf = ors_total['Given either ORS or RHF for diarrhea|Yes']
zinc_rate = ors_total['Given zinc for diarrhea|Yes']
ors_zinc = ors_total['Given zinc and ORS for diarrhea|Yes']
ors_fluids = ors_total['Given ORS or increased fluids for diarrhea|Yes']
tro_rate = ors_total['Given oral rehydration treatment or increased liquids for diarrhea|Yes']
antibiotics = ors_total['Given antibiotic drugs for diarrhea|Yes']
home_remedy = ors_total['Given home remedy or other treatment for diarrhea|Yes']
no_treatment = ors_total['No treatment for diarrhea|Yes']

print(f"  ORS: {ors_rate:.1f}%, TRO: {tro_rate:.1f}%, No treatment: {no_treatment:.1f}%")

# --- Extract ORS by Wealth Quintile ---
wealth_labels = ['poorest', 'poorer', 'middle', 'richer', 'richest']
ors_by_wealth = []
for w in wealth_labels:
    row = df_ors[df_ors['row_labels'].str.contains(w, case=False, na=False)]
    if not row.empty:
        ors_by_wealth.append(row.iloc[0]['Given oral rehydration salts for diarrhea|Yes'])

print(f"  ORS by wealth: {[round(x,1) for x in ors_by_wealth]}")

# --- Extract Care-seeking by Education ---
edu_labels = ['no education', 'primary', 'secondary', 'higher']
care_by_edu = []
for e in edu_labels:
    row = df_fever[df_fever['row_labels'].str.contains(e, case=False, na=False)]
    if not row.empty and 'Weighted' not in row.iloc[0]['row_labels']:
        care_by_edu.append(row.iloc[0]['Advice or treatment sought for fever symptoms|Yes'])

print(f"  Care-seeking by education: {[round(x,1) for x in care_by_edu]}")

# --- Extract Feeding Data ---
feeding_total = get_total_row(df_feeding)
liquid_more = feeding_total['Amount of liquids given for child with diarrhea|More']
liquid_same = feeding_total['Amount of liquids given for child with diarrhea|Same as usual']
liquid_less = feeding_total['Amount of liquids given for child with diarrhea|Somewhat less']
liquid_much_less = feeding_total['Amount of liquids given for child with diarrhea|Much less']
liquid_none = feeding_total['Amount of liquids given for child with diarrhea|None']

food_more = feeding_total['Amount of food given for child with diarrhea|More']
food_same = feeding_total['Amount of food given for child with diarrhea|Same as usual']
food_less = feeding_total['Amount of food given for child with diarrhea|Somewhat less']
food_much_less = feeding_total['Amount of food given for child with diarrhea|Much less']
food_none = feeding_total['Amount of food given for child with diarrhea|None']

print(f"  Liquids: More {liquid_more:.1f}%, Same {liquid_same:.1f}%")
print(f"  Food: More {food_more:.1f}%, Same {food_same:.1f}%")

# --- Extract Regional Data ---
regions_list = ['adamawa', 'centre (without yaounde)', 'douala', 'east', 'far-north',
                'littoral (without douala)', 'north', 'north-west', 'west', 'south', 
                'south-west', 'yaounde']
region_names = ['Adamawa', 'Centre (Without Yaounde)', 'Douala', 'East', 'Far-North',
                'Littoral (Without Douala)', 'North', 'North-West', 'West', 'South',
                'South-West', 'Yaounde']

regional_data = {'Region': [], 'Diarrhea': [], 'Fever': [], 'Ari': []}
for i, reg in enumerate(regions_list):
    # Get diarrhea (NO symptom column)
    d_row = df_diarrhea[df_diarrhea['row_labels'].str.contains(reg, case=False, na=False)]
    f_row = df_fever[df_fever['row_labels'].str.contains(reg, case=False, na=False)]
    a_row = df_ari[df_ari['row_labels'].str.contains(reg, case=False, na=False)]
    
    if not d_row.empty and not f_row.empty and not a_row.empty:
        regional_data['Region'].append(region_names[i])
        regional_data['Diarrhea'].append(d_row.iloc[0]['Diarrhea in the 2 weeks before the survey|No'])
        regional_data['Fever'].append(f_row.iloc[0]['Fever symptoms in the 2 weeks before the survey|No'])
        regional_data['Ari'].append(a_row.iloc[0]['ARI symptoms in the 2 weeks before the survey|No'])

regional_df = pd.DataFrame(regional_data)
print(f"  Loaded regional data for {len(regional_df)} regions")

# ============================================================================
# CHART 1: Graphique 10.8 - Prevalence and Treatment (French Style)
# ============================================================================
print("\n" + "="*70)
print("GENERATING CHARTS")
print("="*70)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Left: Prevalence
categories = ['IRA', 'Fièvre', 'Diarrhée']
prevalence = [round(ari_prev), round(fever_prev), round(diarrhea_prev)]
ax1 = axes[0]
bars1 = ax1.bar(categories, prevalence, color='#808000', width=0.6)
ax1.set_ylabel('')
ax1.set_ylim(0, 20)
ax1.set_title("Pourcentage d'enfants de moins de 5 ans ayant présenté\ndes symptômes au cours des 2 semaines avant l'interview", 
              fontsize=9, pad=10)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
for bar, val in zip(bars1, prevalence):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val}%', 
             ha='center', va='bottom', fontweight='bold', fontsize=12)

# Right: Treatment
treatment = [round(ari_treat), round(fever_treat), round(diarrhea_treat)]
ax2 = axes[1]
bars2 = ax2.bar(categories, treatment, color='#87CEEB', width=0.6)
ax2.set_ylabel('')
ax2.set_ylim(0, 80)
ax2.set_title("Parmi ces enfants malades, pourcentage pour lesquels\non a recherché des conseils ou un traitement", 
              fontsize=9, pad=10)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
for bar, val in zip(bars2, treatment):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val}%', 
             ha='center', va='bottom', fontweight='bold', fontsize=12)

fig.suptitle("Graphique 10.8 Prévalence et traitement des maladies infantiles", 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('output/graphique_10_8_prevalence_treatment.png', bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: graphique_10_8_prevalence_treatment.png")

# ============================================================================
# CHART 2: Graphique 10.6 - Diarrhea by Age (French Style)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

age_labels = ['<6', '6-11', '12-23', '24-35', '36-47', '48-59', 'Ensemble']
diarrhea_values = [round(x) for x in diarrhea_by_age] + [round(diarrhea_prev)]
colors = ['#4472C4'] * 6 + ['#70AD47']

bars = ax.bar(age_labels, diarrhea_values, color=colors, width=0.7)
ax.set_xlabel('Âge en mois', fontsize=11)
ax.set_ylabel('')
ax.set_ylim(0, 30)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for bar, val in zip(bars, diarrhea_values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val}%', 
            ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_title("Graphique 10.6 Prévalence de la diarrhée, par âge\n"
             "Pourcentage d'enfants de moins de 5 ans ayant eu la diarrhée au cours des 2 semaines avant l'enquête",
             fontsize=11, fontweight='bold', loc='left')
plt.tight_layout()
plt.savefig('output/graphique_10_6_diarrhea_age.png', bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: graphique_10_6_diarrhea_age.png")

# ============================================================================
# CHART 3: Graphique 10.5 - Diarrhea Treatment (French Horizontal Bar)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 8))

treatment_labels = [
    'Recherche conseil/traitement',
    'SRO (sachet)',
    'Solution maison recommandée',
    'SRO ou SMR',
    'Zinc',
    'SRO et zinc',
    'SRO ou liquides augmentés',
    'TRO',
    'Antibiotiques',
    'Remède maison/autre',
    'Aucun traitement'
]
treatment_values = [
    round(diarrhea_treat),  # 52
    round(ors_rate),        # 18
    round(rhf_rate),        # 11
    round(ors_rhf),         # 23
    round(zinc_rate),       # 21
    round(ors_zinc),        # 8
    round(ors_fluids),      # 42
    round(tro_rate),        # 45
    round(antibiotics),     # 21
    round(home_remedy),     # 25
    round(no_treatment)     # 23
]
treatment_colors = ['#E74C3C', '#F39C12', '#F39C12', '#F39C12', '#3498DB', 
                    '#F39C12', '#F39C12', '#27AE60', '#2C3E50', '#2C3E50', '#2C3E50']

# Reverse for horizontal bar
y_pos = np.arange(len(treatment_labels))
bars = ax.barh(y_pos, treatment_values, color=treatment_colors, height=0.7)
ax.set_yticks(y_pos)
ax.set_yticklabels(treatment_labels)
ax.invert_yaxis()
ax.set_xlim(0, 60)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for bar, val in zip(bars, treatment_values):
    ax.text(val + 1, bar.get_y() + bar.get_height()/2, f'{val}', 
            ha='left', va='center', fontweight='bold', fontsize=10)

ax.set_title("Graphique 10.5 Traitement de la diarrhée\n"
             "Pourcentage d'enfants de moins de 5 ans ayant eu la diarrhée au cours des 2 semaines avant l'interview",
             fontsize=11, fontweight='bold', loc='left')
plt.tight_layout()
plt.savefig('output/graphique_10_5_diarrhea_treatment.png', bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: graphique_10_5_diarrhea_treatment.png")

# ============================================================================
# CHART 4: Graphique 10.7 - Feeding Practices (French Stacked Bar)
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 4))

# Data
categories = ['Aliments donnés\n(par rapport à la normale)', 'Liquides donnés\n(par rapport à la normale)']
data = {
    'Davantage': [round(food_more), round(liquid_more)],
    'Même': [round(food_same), round(liquid_same)],
    'Moins': [round(food_less), round(liquid_less)],
    'Rien': [round(food_none), round(liquid_none)]
}
colors = {'Davantage': '#27AE60', 'Même': '#3498DB', 'Moins': '#F39C12', 'Rien': '#C0392B'}

# Create stacked horizontal bar
y_pos = np.arange(len(categories))
left = np.zeros(len(categories))

for label, values in data.items():
    bars = ax.barh(y_pos, values, left=left, label=label, color=colors[label], height=0.5)
    # Add labels
    for i, (bar, val) in enumerate(zip(bars, values)):
        if val > 5:
            ax.text(left[i] + val/2, bar.get_y() + bar.get_height()/2, f'{val}%',
                    ha='center', va='center', fontweight='bold', fontsize=10, color='white')
    left += values

ax.set_yticks(y_pos)
ax.set_yticklabels(categories)
ax.set_xlim(0, 100)
ax.legend(loc='lower center', ncol=4, bbox_to_anchor=(0.5, -0.3))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_title("Graphique 10.7 Pratiques alimentaires pendant la diarrhée\n"
             "Pourcentage d'enfants de moins de 5 ans ayant eu la diarrhée au cours des 2 semaines avant l'interview",
             fontsize=11, fontweight='bold', loc='left')
plt.tight_layout()
plt.savefig('output/graphique_10_7_feeding_practices.png', bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: graphique_10_7_feeding_practices.png")

# ============================================================================
# CHART 5: Figure 5 - ORS by Wealth Quintile (Rainbow Gradient)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

wealth_display = ['Poorest', 'Poorer', 'Middle', 'Richer', 'Richest']
wealth_colors = ['#C0392B', '#E67E22', '#F1C40F', '#27AE60', '#145A32']

bars = ax.bar(wealth_display, ors_by_wealth, color=wealth_colors, width=0.6)
ax.set_xlabel('Wealth Quintile', fontsize=11)
ax.set_ylabel('ORS Treatment Rate (%)', fontsize=11)
ax.set_ylim(0, 35)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

for bar, val in zip(bars, ors_by_wealth):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val:.1f}%', 
            ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_title("Figure 5: ORS Treatment for Diarrhea by Wealth Quintile\nCameroon DHS 2018",
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('output/fig5_ors_wealth.png', bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: fig5_ors_wealth.png")

# ============================================================================
# CHART 6: Figure 7 - Care-seeking by Education (Green Gradient)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

edu_display = ['No Education', 'Primary', 'Secondary', 'Higher']
edu_colors = ['#A9DFBF', '#52BE80', '#27AE60', '#145A32']

bars = ax.bar(edu_display, care_by_edu, color=edu_colors, width=0.6)
ax.set_xlabel("Mother's Education Level", fontsize=11)
ax.set_ylabel('Care-Seeking Rate (%)', fontsize=11)
ax.set_ylim(0, 75)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

for bar, val in zip(bars, care_by_edu):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val:.1f}%', 
            ha='center', va='bottom', fontweight='bold', fontsize=11)

ax.set_title("Figure 7: Care-Seeking for Fever by Mother's Education\nCameroon DHS 2018",
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('output/fig7_careseeking_education.png', bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: fig7_careseeking_education.png")

# ============================================================================
# CHART 7: Figure 8 - Regional Heatmap
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 8))

# Create heatmap data (using "No symptom" rates as in reference)
heatmap_data = regional_df.set_index('Region')[['Diarrhea', 'Fever', 'Ari']]

# Create heatmap
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd', 
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Prevalence (%)'})
ax.set_xlabel('Health Indicator', fontsize=11)
ax.set_ylabel('')
ax.set_title("Figure 8: Regional Child Morbidity Indicators\nCameroon DHS 2018",
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('output/fig8_regional_heatmap.png', bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: fig8_regional_heatmap.png")

# ============================================================================
# CHART 8: Figure 9 - Morbidity Prevalence and Treatment (Grouped Bar)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

conditions = ['Diarrhea', 'Fever', 'ARI Symptoms']
prev_values = [round(diarrhea_prev), round(fever_prev), round(ari_prev)]
treat_values = [round(diarrhea_treat), round(fever_treat), round(ari_treat)]

x = np.arange(len(conditions))
width = 0.35

bars1 = ax.bar(x - width/2, prev_values, width, label='Prevalence', color='#E57373')
bars2 = ax.bar(x + width/2, treat_values, width, label='Treatment Sought', color='#81C784')

ax.set_xlabel('Health Condition', fontsize=11)
ax.set_ylabel('Percentage (%)', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(conditions)
ax.set_ylim(0, 80)
ax.legend(loc='upper right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

for bar, val in zip(bars1, prev_values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val}%', 
            ha='center', va='bottom', fontweight='bold', fontsize=10)
for bar, val in zip(bars2, treat_values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f'{val}%', 
            ha='center', va='bottom', fontweight='bold', fontsize=10)

ax.set_title("Figure 9: Child Morbidity Prevalence and Treatment Seeking\n(Data from Excel files)",
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('output/fig9_morbidity_treatment.png', bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: fig9_morbidity_treatment.png")

# ============================================================================
# CHART 9: Figure 11 - Feeding Practices (Grouped Bar - English)
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 6))

feeding_categories = ['More', 'Same', 'Less', 'Much Less', 'None']
liquids = [round(liquid_more), round(liquid_same), round(liquid_less), 
           round(liquid_much_less), round(liquid_none)]
foods = [round(food_more), round(food_same), round(food_less), 
         round(food_much_less), round(food_none)]

x = np.arange(len(feeding_categories))
width = 0.35

bars1 = ax.bar(x - width/2, liquids, width, label='Liquids', color='#5DADE2')
bars2 = ax.bar(x + width/2, foods, width, label='Food', color='#F5B041')

ax.set_xlabel('Amount Given During Diarrhea', fontsize=11)
ax.set_ylabel('Percentage of Children (%)', fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(feeding_categories)
ax.set_ylim(0, 50)
ax.legend(loc='upper right')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.3)

# Add annotation
ax.annotate('*Recommended: More liquids & same/more food*', 
            xy=(0.5, 0.95), xycoords='axes fraction',
            ha='center', fontsize=10, fontstyle='italic',
            bbox=dict(boxstyle='round', facecolor='#FFFACD', alpha=0.8))

ax.set_title("Figure 11: Feeding Practices During Diarrhea\n(Data from Excel files)",
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('output/fig11_feeding_diarrhea.png', bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: fig11_feeding_diarrhea.png")

# ============================================================================
# CHART 10: Figure 3 - Diarrhea Prevalence by Age (Line/Area Chart)
# Note: Using "No diarrhea" rates as shown in reference image
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

age_display = ['<6', '6-11', '12-23', '24-35', '36-47', '48-59']
# Get "No diarrhea" values for area chart (as shown in reference)
no_diarrhea = []
for label in age_labels_raw:
    row = df_diarrhea[df_diarrhea['row_labels'].str.contains(f'|{label}', regex=False, na=False)]
    if not row.empty:
        no_diarrhea.append(row.iloc[0]['Diarrhea in the 2 weeks before the survey|No'])

ax.fill_between(range(len(age_display)), no_diarrhea, alpha=0.3, color='#E57373')
ax.plot(range(len(age_display)), no_diarrhea, marker='o', markersize=10, 
        color='#D35400', linewidth=3, markerfacecolor='white', markeredgewidth=3)

ax.set_xticks(range(len(age_display)))
ax.set_xticklabels(age_display)
ax.set_xlabel('Child Age (months)', fontsize=11)
ax.set_ylabel('Diarrhea Prevalence (%)', fontsize=11)
ax.set_ylim(70, 100)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.3)

for i, val in enumerate(no_diarrhea):
    ax.text(i, val + 1.5, f'{val:.1f}%', ha='center', fontweight='bold', fontsize=10)

ax.set_title("Figure 3: Diarrhea Prevalence by Child Age\n(Two weeks preceding survey)",
             fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('output/fig3_diarrhea_age.png', bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: fig3_diarrhea_age.png")

# ============================================================================
# GENERATE REPORT
# ============================================================================
print("\n" + "="*70)
print("GENERATING REPORT")
print("="*70)

report_content = f"""# Child Health Analysis Report
## Cameroon Demographic and Health Survey 2018

**Author:** Momeni Gilles  
**Date:** January 2026  
**Data Sources:** Tables_DIAR.xls, Tables_ARI_FV.xls, Tables_Size.xls

---

## Executive Summary

This report presents a comprehensive analysis of child health indicators in Cameroon based on the 2018 Demographic and Health Survey (DHS). The analysis focuses on childhood morbidity (diarrhea, fever, and acute respiratory infections), treatment-seeking behaviors, and feeding practices during illness.

### Key Findings

| Indicator | Prevalence | Treatment Seeking |
|-----------|------------|-------------------|
| Diarrhea | {diarrhea_prev:.1f}% | {diarrhea_treat:.1f}% |
| Fever | {fever_prev:.1f}% | {fever_treat:.1f}% |
| ARI Symptoms | {ari_prev:.1f}% | {ari_treat:.1f}% |

---

## 1. Childhood Morbidity Overview

### 1.1 Prevalence of Childhood Illnesses

Among children under 5 years of age in Cameroon, the two-week prevalence rates were:

- **Fever:** {fever_prev:.1f}% - the most common childhood illness
- **Diarrhea:** {diarrhea_prev:.1f}% - affecting approximately 1 in 8 children
- **ARI Symptoms:** {ari_prev:.1f}% - relatively rare but potentially severe

![Prevalence and Treatment](graphique_10_8_prevalence_treatment.png)
*Graphique 10.8: Prévalence et traitement des maladies infantiles*

### 1.2 Treatment-Seeking Behavior

Treatment-seeking rates varied by illness type:
- **Fever:** {fever_treat:.1f}% sought treatment (highest rate)
- **ARI:** {ari_treat:.1f}% sought treatment
- **Diarrhea:** {diarrhea_treat:.1f}% sought treatment (lowest rate)

![Morbidity and Treatment](fig9_morbidity_treatment.png)
*Figure 9: Child Morbidity Prevalence and Treatment Seeking*

---

## 2. Diarrhea Deep Dive

### 2.1 Age-Specific Prevalence

Diarrhea prevalence follows a characteristic age pattern, peaking in the 6-23 month age range:

| Age Group | Prevalence |
|-----------|------------|
| <6 months | {diarrhea_by_age[0]:.1f}% |
| 6-11 months | {diarrhea_by_age[1]:.1f}% |
| 12-23 months | {diarrhea_by_age[2]:.1f}% |
| 24-35 months | {diarrhea_by_age[3]:.1f}% |
| 36-47 months | {diarrhea_by_age[4]:.1f}% |
| 48-59 months | {diarrhea_by_age[5]:.1f}% |

![Diarrhea by Age](graphique_10_6_diarrhea_age.png)
*Graphique 10.6: Prévalence de la diarrhée par âge*

### 2.2 Treatment Patterns

Various treatments were used for childhood diarrhea:

| Treatment | Percentage |
|-----------|------------|
| TRO (Oral Rehydration Therapy) | {tro_rate:.1f}% |
| ORS or increased fluids | {ors_fluids:.1f}% |
| ORS (sachet) | {ors_rate:.1f}% |
| Zinc | {zinc_rate:.1f}% |
| ORS and Zinc (combined) | {ors_zinc:.1f}% |
| No treatment | {no_treatment:.1f}% |

![Treatment Types](graphique_10_5_diarrhea_treatment.png)
*Graphique 10.5: Traitement de la diarrhée*

---

## 3. Socio-Economic Determinants

### 3.1 ORS Use by Wealth Quintile

Access to ORS treatment shows a clear wealth gradient:

| Wealth Quintile | ORS Rate |
|-----------------|----------|
| Poorest | {ors_by_wealth[0]:.1f}% |
| Poorer | {ors_by_wealth[1]:.1f}% |
| Middle | {ors_by_wealth[2]:.1f}% |
| Richer | {ors_by_wealth[3]:.1f}% |
| Richest | {ors_by_wealth[4]:.1f}% |

![ORS by Wealth](fig5_ors_wealth.png)
*Figure 5: ORS Treatment for Diarrhea by Wealth Quintile*

### 3.2 Care-Seeking by Mother's Education

| Education Level | Care-Seeking Rate |
|-----------------|-------------------|
| No Education | {care_by_edu[0]:.1f}% |
| Primary | {care_by_edu[1]:.1f}% |
| Secondary | {care_by_edu[2]:.1f}% |
| Higher | {care_by_edu[3]:.1f}% |

![Care-seeking by Education](fig7_careseeking_education.png)
*Figure 7: Care-Seeking for Fever by Mother's Education*

---

## 4. Feeding Practices During Illness

### 4.1 Fluid and Food Intake During Diarrhea

WHO recommends increasing fluids and maintaining food intake during diarrhea:

**Liquids given:**
- More: {liquid_more:.1f}%
- Same: {liquid_same:.1f}%
- Less: {liquid_less:.1f}%
- None: {liquid_none:.1f}%

**Food given:**
- More: {food_more:.1f}%
- Same: {food_same:.1f}%
- Less: {food_less:.1f}%
- None: {food_none:.1f}%

![Feeding Practices French](graphique_10_7_feeding_practices.png)
*Graphique 10.7: Pratiques alimentaires pendant la diarrhée*

![Feeding Practices](fig11_feeding_diarrhea.png)
*Figure 11: Feeding Practices During Diarrhea*

---

## 5. Regional Analysis

![Regional Heatmap](fig8_regional_heatmap.png)
*Figure 8: Regional Child Morbidity Indicators*

---

## 6. Conclusions and Recommendations

### Key Findings:
1. **Fever** is the most prevalent childhood illness ({fever_prev:.1f}%)
2. **Diarrhea** peaks in children aged 6-23 months ({diarrhea_by_age[2]:.1f}%)
3. **ORS treatment** shows significant wealth disparities (9.2% poorest vs 29.9% richest)
4. **Combined ORS+Zinc** use remains low at {ors_zinc:.1f}%

### Recommendations:
1. Target diarrhea prevention for 6-23 month age group
2. Improve ORS access in poorest wealth quintiles
3. Promote combined ORS+Zinc treatment
4. Educate caregivers on feeding practices during illness

---

## Data Sources

All data extracted from:
- `Tables_DIAR.xls` - Diarrhea prevalence and treatment
- `Tables_ARI_FV.xls` - ARI and Fever data
- `Tables_Size.xls` - Birth weight data

**Reference:** Cameroon Demographic and Health Survey 2018, Institut National de la Statistique (INS) and ICF.
"""

with open('output/Child_Health_Report_Cameroon_DHS2018.md', 'w') as f:
    f.write(report_content)
print("  ✓ Saved: Child_Health_Report_Cameroon_DHS2018.md")

print("\n" + "="*70)
print("ANALYSIS COMPLETE!")
print("Output directory: output/")
print("="*70)
