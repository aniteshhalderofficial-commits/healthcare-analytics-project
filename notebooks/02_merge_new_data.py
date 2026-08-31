import pandas as pd
import requests
import sqlite3

# 1. Define the new indicators to pull from World Bank
new_indicators = {
    "SH.MED.BEDS.ZS": "hospital_beds_per_1000",
    "SH.STA.BASS.ZS": "sanitation_access_pct",
    "EN.ATM.CO2E.PC": "co2_emissions_per_capita"
}

countries = "all"
years = "2000:2023"
new_data_frames = []

print("Fetching new datasets from World Bank API...")
for code, name in new_indicators.items():
    url = f"http://api.worldbank.org/v2/country/{countries}/indicator/{code}?date={years}&format=json&per_page=10000"
    response = requests.get(url).json()
    
    if len(response) > 1:
        data = response[1]
        df = pd.DataFrame(data)
        # Extract country name and clean up columns
        df['country'] = df['country'].apply(lambda x: x['value'])
        df = df[['country', 'date', 'value']].rename(columns={'date': 'year', 'value': name})
        df['year'] = df['year'].astype(int)
        new_data_frames.append(df)

# Merge all new indicators into a single DataFrame
merged_new_data = new_data_frames[0]
for df in new_data_frames[1:]:
    merged_new_data = pd.merge(merged_new_data, df, on=['country', 'year'], how='outer')

# 2. Connect to Database and Load Existing Data
print("Loading existing database...")
conn = sqlite3.connect("database/healthcare.db")
existing_df = pd.read_sql_query("SELECT * FROM health_metrics", conn)

# 3. Perform the Advanced JOIN (Merge)
print("Merging datasets...")
# We use a LEFT JOIN to keep our original dataset intact and just append the new columns where they match
final_df = pd.merge(existing_df, merged_new_data, on=['country', 'year'], how='left')

# 4. Save back to SQL Database
final_df.to_sql("health_metrics", conn, if_exists="replace", index=False)
conn.close()

print("Success! Database updated with new variables.")
print(final_df.head())