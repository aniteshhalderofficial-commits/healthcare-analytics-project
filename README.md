# 🌍 Global Health & Life Expectancy Predictor

## Project Overview
This project is an end-to-end data science pipeline that analyzes and forecasts the relationship between a country's economic output, healthcare infrastructure, and the life expectancy of its citizens. 

Originally an exploratory data analysis of health expenditure, the project has evolved into a fully automated multivariate machine learning application. It extracts data from the World Bank API, processes it through a local SQLite database, trains an `ExtraTreesRegressor` model, and serves interactive predictions via a Streamlit dashboard.

**Data Source:** World Bank API (Economics, Healthcare Capacity, and Sanitation data).

## Tech Stack
* **Language:** Python
* **Data Engineering:** SQLite3, Pandas, Requests (REST API)
* **Machine Learning:** Scikit-Learn (ExtraTreesRegressor, KNNImputer, StandardScaler)
* **Web App Deployment:** Streamlit
* **Visualization:** Matplotlib, Seaborn, Streamlit native charts

## Core Pipeline

1. **Automated Data Extraction & ETL:** Python scripts fetch historical metrics (GDP, Health Expenditure, Physicians, Hospital Beds, Sanitation Access) directly from the World Bank API, transforming and storing them in a relational SQLite database.
2. **Multivariate Merging:** Eliminates omitted variable bias by performing advanced SQL/Pandas joins to combine economic indicators with physical infrastructure and hygiene metrics.
3. **Machine Learning Forecasting:** Missing values are handled via KNN Imputation. An Extra Trees Regressor is trained on scaled historical data to capture complex, non-linear relationships between financial investment, infrastructure, and health outcomes.
4. **Interactive Dashboard:** A Streamlit UI allows users to select country presets, manipulate future economic and infrastructure variables via sliders, and instantly visualize predicted life expectancy trajectories up to the year 2030.

## Key Insights
* **The Infrastructure Premium:** Factoring in non-financial metrics like basic sanitation access and hospital bed capacity significantly improves model accuracy, demonstrating that physical infrastructure limits or boosts the effectiveness of raw GDP.
* **General Correlation:** For developing and middle-income nations, increased health expenditure and sanitation improvements demonstrate a strong positive correlation with rising life expectancy.
* **The Efficiency Gap (The U.S. Outlier):** Historical data reveals a significant efficiency gap in the United States. Despite spending drastically more per capita than any other analyzed nation, U.S. life expectancy remains lower than nations like Japan and Germany, which spend approximately half as much but achieve life expectancies in the 80+ year range.

## Project Structure
* `app.py`: The main Streamlit application for the interactive forecasting dashboard.
* `database/`: Contains the local `healthcare.db` SQLite database (Generated locally, ignored in remote repo).
* `notebooks/`: 
  * `01_load_to_sql.ipynb` / `.py`: API extraction and initial database creation.
  * `02_merge_new_data.py`: Fetches and merges multivariate indicators (Sanitation, Beds) into the database.
  * `03_visualizations.ipynb`: Exploratory data analysis and static plotting.
  * `04_ml_tournament.ipynb`: Evaluates multiple regression algorithms to select the optimal predictive model.

## How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone <https://github.com/aniteshhalderofficial-commits/healthcare-analytics-project>
   cd healthcare-analytics-project