# WASH Under-5 Mortality Data Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://wash-mortality-dashboard-49okovwszkkndcducpw9ns.streamlit.app/)

## Overview
An interactive data visualization dashboard examining global under-5 child mortality rates linked to Unsafe Water, Sanitation, and Hygiene (WASH) practices using World Bank Data360 dataset (2019). The project delivers evidence-informed insights into environmental health impacts and WASH investment priorities for sustainability stakeholders, financial specialists, and public policy leaders.

Live Streamlit Application: [WASH Mortality Dashboard](https://wash-mortality-dashboard-49okovwszkkndcducpw9ns.streamlit.app/)

## Key Insights & Findings
- **Highest Risk Regions**: Lesotho (108.1 per 1,000 live births), Chad (99.2), and Somalia (99.2) represent the most severe instances requiring targeted aid intervention.
- **Disproportionate Risk Distribution**: While only 7.95% of nations fall into the "Very High" risk category, they account for a significant portion of preventable child fatalities.
- **Global Inequality Gap**: 43.2% of nations are in the "Low" risk category, highlighting both global advancements and severe disparities across developing regions.

## Features
- **Global Geographic Coverage**: Interactive Choropleth map illustrating mortality rates across 176 countries.
- **Dynamic Risk Categorization**: Multi-category filtering (`Low`, `Moderate`, `High`, `Very High`) and numerical range slider controls.
- **Dynamic KPIs**: Real-time KPI summaries for total countries displayed, maximum rate, minimum rate, and global average.
- **Ranked Visualizations**: Sortable Top-N bar charts, donut distribution charts, histograms, and box plots showing variability across categories.
- **Searchable Data Table**: Fast keyword search and filtering across individual country records.

## Tech Stack & Dependencies
- **Language**: Python 3.x
- **Framework**: Streamlit
- **Data Manipulation**: Pandas
- **Interactive Visualizations**: Plotly Express & Plotly Graph Objects

## Dataset Information
- **Source**: World Bank Data360 Platform (`WB WDI SH STA WASH P5`)
- **Scope**: 176 country records across 4 primary features (`Country_Code`, `Country_Name`, `Mortality_Rate_2019`, `Risk_Category`).

## Local Setup & Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AzmaLahir/wash-mortality-dashboard.git
cd wash-mortality-dashboard
   ```

2. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app locally**:
   ```bash
   streamlit run app.py
   ```
