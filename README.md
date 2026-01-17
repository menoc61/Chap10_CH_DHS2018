# Cameroon DHS 2018 - Child Health Analysis

## Overview

Comprehensive analysis of child health indicators in Cameroon based on the Demographic and Health Survey (DHS) 2018. This project focuses on childhood morbidity (diarrhea, fever, acute respiratory infections), treatment-seeking behaviors, feeding practices, and socio-economic determinants.

## Data Sources

| File | Description |
|------|-------------|
| `Tables_DIAR.xls` | Diarrhea prevalence, treatment, ORS usage, feeding practices |
| `Tables_ARI_FV.xls` | ARI and fever prevalence and treatment data |
| `Tables_Size.xls` | Birth weight and size at birth data |
| `chap 10.pdf` | DHS Chapter 10 reference document |

## Key Findings

### Morbidity Prevalence (2-week recall)
| Condition | Prevalence | Treatment Rate |
|-----------|------------|----------------|
| Fever | 15.4% | 61.0% |
| Diarrhea | 11.9% | 51.6% |
| ARI | 1.0% | 59.2% |

### Key Insights
- **Peak diarrhea age**: 12-23 months (21.1%)
- **ORS disparity**: Poorest 9.2% vs Richest 29.9%
- **Combined ORS+Zinc**: Only 7.7%

## Generated Charts

### French Style (Official DHS Format)
| File | Description |
|------|-------------|
| `graphique_10_8_prevalence_treatment.png` | Prevalence & treatment comparison |
| `graphique_10_6_diarrhea_age.png` | Diarrhea by age group |
| `graphique_10_5_diarrhea_treatment.png` | Treatment types (horizontal bars) |
| `graphique_10_7_feeding_practices.png` | Feeding practices (stacked bars) |

### English Style (Modern Charts)
| File | Description |
|------|-------------|
| `fig3_diarrhea_age.png` | Age prevalence area chart |
| `fig5_ors_wealth.png` | ORS by wealth quintile (rainbow) |
| `fig7_careseeking_education.png` | Care-seeking by education (green) |
| `fig8_regional_heatmap.png` | Regional morbidity heatmap |
| `fig9_morbidity_treatment.png` | Morbidity grouped bar chart |
| `fig11_feeding_diarrhea.png` | Feeding practices (liquids/food) |

## Project Structure

```
/workspace/
├── cameroon_dhs2018_child_health_analysis.py   # Main analysis script
├── README.md                                    # This documentation
│
├── output/                                      # Generated outputs
│   ├── Child_Health_Report_Cameroon_DHS2018.pdf
│   ├── Child_Health_Report_Cameroon_DHS2018.docx
│   ├── Child_Health_Report_Cameroon_DHS2018.md
│   │
│   ├── graphique_10_8_prevalence_treatment.png
│   ├── graphique_10_6_diarrhea_age.png
│   ├── graphique_10_5_diarrhea_treatment.png
│   ├── graphique_10_7_feeding_practices.png
│   │
│   ├── fig3_diarrhea_age.png
│   ├── fig5_ors_wealth.png
│   ├── fig7_careseeking_education.png
│   ├── fig8_regional_heatmap.png
│   ├── fig9_morbidity_treatment.png
│   └── fig11_feeding_diarrhea.png
│
└── user_input_files/                            # Source data
    ├── Tables_DIAR.xls
    ├── Tables_ARI_FV.xls
    ├── Tables_Size.xls
    └── chap 10.pdf
```

## Requirements

```
Python 3.8+
pandas
matplotlib
seaborn
openpyxl / xlrd
```

## Usage

```bash
python cameroon_dhs2018_child_health_analysis.py
```

**Output:**
1. Extracts data from Excel files
2. Generates 10 visualizations
3. Creates Markdown report

## Methodology

### Data Extraction
All values are dynamically extracted from DHS tabulation Excel files using "Total" rows. No hardcoded data.

### Color Schemes
| Element | Color |
|---------|-------|
| Prevalence | Olive Green (#808000) |
| Treatment | Sky Blue (#87CEEB) |
| Age groups | Blue (#4472C4) |
| Total/Ensemble | Green (#70AD47) |
| Wealth (poor to rich) | Red to Yellow to Green |
| Education | Light to Dark Green |

## Citation

> Cameroon Demographic and Health Survey 2018.  
> Institut National de la Statistique (INS) and ICF.

## Author

**Momeni Gilles** | January 2026
