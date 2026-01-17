# Comprehensive Child Health Analysis

This project analyzes child health indicators using data from the Cameroon DHS survey.

## Project Structure
- `comprehensive_child_health_analysis.py`: Main Python script for analysis
- `CH_*.R`, `CHmain.R`, `chapter10_child_health_analysis.R`: R scripts for additional analyses
- `CMIR71FL.dta`, `CMKR71FL.dta`: Data files (Stata format)
- `output/`: Output reports and results
- `user_input_files/`: Place for user-supplied files

## Requirements
Install dependencies with:

    pip install -r requirements.txt

## Usage
Run the main analysis script:

    python comprehensive_child_health_analysis.py

## Notes
- Some data may require Excel support; ensure `xlrd` and `openpyxl` are installed.
- R scripts require R and relevant R packages.

## Author
- Momeni Gilles
