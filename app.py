import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer

st.set_page_config(page_title="Global Health Predictor", layout="wide")

# --- 1. Load Expanded Data & Train Model ---
@st.cache_resource
def load_and_train():
    conn = sqlite3.connect("database/healthcare.db", timeout=10)
    # Removed co2_emissions_per_capita to match actual database schema
    query = """
    SELECT country, year, life_expectancy, health_expenditure, gdp_per_capita, 
           physicians_per_1000, hospital_beds_per_1000, sanitation_access_pct
    FROM health_metrics
    WHERE life_expectancy IS NOT NULL;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Feature Engineering
    df["log_health_expenditure"] = np.log1p(df["health_expenditure"])
    df["log_gdp_per_capita"] = np.log1p(df["gdp_per_capita"])
    df["health_gdp_ratio"] = df["health_expenditure"] / df["gdp_per_capita"]

    # Removed CO2 from feature list
    features = [
        "year", "log_health_expenditure", "log_gdp_per_capita", "health_gdp_ratio", 
        "physicians_per_1000", "hospital_beds_per_1000", "sanitation_access_pct"
    ]
    
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

# --- 2. Dashboard UI Header ---
st.title("🌍 Global Health & Life Expectancy Multivariate Predictor")
st.markdown("This enhanced model factors in **economic output, healthcare spending, doctor/bed capacity, and sanitation coverage** to predict life expectancy trends through 2030.")

# Country Preset Selection
country_list = sorted(df['country'].unique())
selected_country = st.selectbox("📌 Select Country Preset:", country_list, index=country_list.index("India") if "India" in country_list else 0)

latest_country_df = df[df['country'] == selected_country].sort_values(by="year", ascending=False)
latest_country_data = latest_country_df.iloc[0]
latest_year = int(latest_country_data["year"])
latest_actual_le = latest_country_data["life_expectancy"]

# --- 3. Sidebar Configuration ---
st.sidebar.header(f"Configure Variables ({selected_country})")

input_year = st.sidebar.slider("Target Forecast Year", min_value=latest_year, max_value=2030, value=2030)
input_gdp = st.sidebar.number_input("GDP per Capita ($)", min_value=100.0, max_value=150000.0, value=float(round(latest_country_data["gdp_per_capita"] or 2000.0, 2)), step=500.0)
input_health_exp = st.sidebar.number_input("Health Spending per Capita ($)", min_value=10.0, max_value=20000.0, value=float(round(latest_country_data["health_expenditure"] or 100.0, 2)), step=100.0)

phys_default = float(round(latest_country_data["physicians_per_1000"], 2)) if pd.notnull(latest_country_data["physicians_per_1000"]) else 2.5
beds_default = float(round(latest_country_data["hospital_beds_per_1000"], 2)) if pd.notnull(latest_country_data["hospital_beds_per_1000"]) else 1.5
sanit_default = float(round(latest_country_data["sanitation_access_pct"], 1)) if pd.notnull(latest_country_data["sanitation_access_pct"]) else 70.0

input_physicians = st.sidebar.slider("Physicians (per 1,000 people)", min_value=0.0, max_value=10.0, value=phys_default, step=0.1)
input_beds = st.sidebar.slider("Hospital Beds (per 1,000 people)", min_value=0.0, max_value=15.0, value=beds_default, step=0.1)
input_sanitation = st.sidebar.slider("Basic Sanitation Access (%)", min_value=0.0, max_value=100.0, value=sanit_default, step=1.0)

# --- 4. Model Prediction Execution ---
log_health = np.log1p(input_health_exp)
log_gdp = np.log1p(input_gdp)
ratio = input_health_exp / input_gdp

user_input_raw = pd.DataFrame([[
    input_year, log_health, log_gdp, ratio, 
    input_physicians, input_beds, input_sanitation
]], columns=features)

user_input_imp = imputer.transform(user_input_raw)
user_input_scaled = scaler.transform(user_input_imp)
target_prediction = model.predict(user_input_scaled)[0]

# --- 5. Summary Scorecards ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label=f"Predicted Life Expectancy ({input_year})", value=f"{target_prediction:.1f} Yrs", delta=f"{(target_prediction - latest_actual_le):+.1f} yrs vs {latest_year}")
with col2:
    st.metric(label=f"Latest Historical Value ({latest_year})", value=f"{latest_actual_le:.1f} Yrs")
with col3:
    st.metric(label="Health Budget % of GDP", value=f"{(ratio * 100):.1f}%")
with col4:
    st.metric(label="Sanitation Level", value=f"{input_sanitation:.1f}%")

st.divider()

# --- 6. Trajectory Forecasting Chart ---
history_df = df[df['country'] == selected_country][['year', 'life_expectancy']].dropna().copy()
history_df.rename(columns={'life_expectancy': 'Historical'}, inplace=True)
history_df['Predicted Scenario'] = np.nan

forecast_years = list(range(latest_year, 2031))
forecast_preds = []

for y in forecast_years:
    sim_raw = pd.DataFrame([[
        y, log_health, log_gdp, ratio, 
        input_physicians, input_beds, input_sanitation
    ]], columns=features)
    sim_imp = imputer.transform(sim_raw)
    sim_scaled = scaler.transform(sim_imp)
    forecast_preds.append(model.predict(sim_scaled)[0])

forecast_df = pd.DataFrame({
    'year': forecast_years,
    'Historical': np.nan,
    'Predicted Scenario': forecast_preds
})

forecast_df.loc[forecast_df['year'] == latest_year, 'Historical'] = latest_actual_le
forecast_df.loc[forecast_df['year'] == latest_year, 'Predicted Scenario'] = latest_actual_le

chart_data = pd.concat([history_df[history_df['year'] < latest_year], forecast_df]).set_index('year')

st.subheader(f"📈 Multivariate Forecast Chart: {selected_country}")
st.line_chart(chart_data, color=["#1f77b4", "#ff4b4b"])