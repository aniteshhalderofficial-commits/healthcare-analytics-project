import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer

st.set_page_config(page_title="Global Health Predictor", layout="wide")

# --- 1. Load Data & Train Model ---
@st.cache_resource
def load_and_train():
    conn = sqlite3.connect("database/healthcare.db", timeout=10)
    query = """
    SELECT country, year, life_expectancy, health_expenditure, gdp_per_capita, physicians_per_1000
    FROM health_metrics
    WHERE health_expenditure IS NOT NULL 
      AND gdp_per_capita IS NOT NULL 
      AND life_expectancy IS NOT NULL;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df["log_health_expenditure"] = np.log1p(df["health_expenditure"])
    df["log_gdp_per_capita"] = np.log1p(df["gdp_per_capita"])
    df["health_gdp_ratio"] = df["health_expenditure"] / df["gdp_per_capita"]

    features = ["year", "log_health_expenditure", "log_gdp_per_capita", "health_gdp_ratio", "physicians_per_1000"]
    X = df[features]
    y = df["life_expectancy"]

    imputer = KNNImputer(n_neighbors=5)
    X_imp = imputer.fit_transform(X)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imp)

    model = ExtraTreesRegressor(n_estimators=100, random_state=42)
    model.fit(X_scaled, y)
    
    return df, model, imputer, scaler, features

df, model, imputer, scaler, features = load_and_train()

# --- 2. Dashboard UI ---
st.title("🌍 Global Health & Life Expectancy Predictor")
st.markdown("Adjust the economic sliders to forecast a country's life expectancy up to **2030**. The chart will map your predictive scenario in **red**.")

# Country Selector
country_list = sorted(df['country'].unique())
selected_country = st.selectbox("📌 Select Country Preset:", country_list, index=country_list.index("India") if "India" in country_list else 0)
latest_country_data = df[df['country'] == selected_country].sort_values(by="year", ascending=False).iloc[0]
latest_year = int(latest_country_data["year"])
latest_actual_le = latest_country_data["life_expectancy"]

# --- 3. Sidebar Inputs ---
st.sidebar.header(f"Future Scenario Metrics")

input_year = st.sidebar.slider("Target Year", min_value=latest_year, max_value=2030, value=2030)
input_gdp = st.sidebar.number_input("GDP per Capita ($)", min_value=100.0, max_value=150000.0, value=float(round(latest_country_data["gdp_per_capita"], 2)), step=500.0)
input_health_exp = st.sidebar.number_input("Health Expenditure per Capita ($)", min_value=10.0, max_value=20000.0, value=float(round(latest_country_data["health_expenditure"], 2)), step=100.0)

phys_val = latest_country_data["physicians_per_1000"]
phys_default = float(round(phys_val, 2)) if pd.notnull(phys_val) else 2.5
input_physicians = st.sidebar.slider("Physicians (per 1000 people)", min_value=0.0, max_value=10.0, value=phys_default, step=0.1)

# --- 4. Process Target Prediction ---
log_health = np.log1p(input_health_exp)
log_gdp = np.log1p(input_gdp)
ratio = input_health_exp / input_gdp

user_data = pd.DataFrame([[input_year, log_health, log_gdp, ratio, input_physicians]], columns=features)
user_data_imp = imputer.transform(user_data)
user_data_scaled = scaler.transform(user_data_imp)
target_prediction = model.predict(user_data_scaled)[0]

# --- 5. Display KPI Metrics ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label=f"Predicted Life Expectancy ({input_year})", value=f"{target_prediction:.1f} Years", delta=f"{(target_prediction - latest_actual_le):+.1f} yrs vs {latest_year}")
with col2:
    st.metric(label=f"Latest Historical Value ({latest_year})", value=f"{latest_actual_le:.1f} Years")
with col3:
    st.metric(label="Simulated Health Budget", value=f"{(ratio * 100):.1f}% of GDP")

st.divider()

# --- 6. Generate Forecast Chart Data ---
# 6a. Get Historical Data
history_df = df[df['country'] == selected_country][['year', 'life_expectancy']].copy()
history_df.rename(columns={'life_expectancy': 'Historical'}, inplace=True)
history_df['Predicted Scenario'] = np.nan

# 6b. Generate Predictions from Latest Year to 2030 based on user sliders
forecast_years = list(range(latest_year, 2031))
forecast_preds = []

for y in forecast_years:
    sim_data = pd.DataFrame([[y, log_health, log_gdp, ratio, input_physicians]], columns=features)
    sim_imp = imputer.transform(sim_data)
    sim_scaled = scaler.transform(sim_imp)
    forecast_preds.append(model.predict(sim_scaled)[0])

forecast_df = pd.DataFrame({
    'year': forecast_years,
    'Historical': np.nan,
    'Predicted Scenario': forecast_preds
})

# Link the lines visually by setting the start of the prediction equal to the end of history
forecast_df.loc[forecast_df['year'] == latest_year, 'Historical'] = latest_actual_le
forecast_df.loc[forecast_df['year'] == latest_year, 'Predicted Scenario'] = latest_actual_le

# Combine and plot
final_chart_df = pd.concat([history_df[history_df['year'] < latest_year], forecast_df]).set_index('year')

st.subheader(f"📈 Forecast Trajectory: {selected_country}")
st.line_chart(final_chart_df, color=["#1f77b4", "#ff4b4b"]) # Blue for historical, Red for prediction