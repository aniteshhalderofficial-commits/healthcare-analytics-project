import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL

doc = docx.Document()

# Page Setup - Margins
sections = doc.sections
for section in sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Colors
PRIMARY = RGBColor(31, 78, 121)    # Deep Navy
SECONDARY = RGBColor(89, 89, 89)   # Slate Grey
TEXT_COLOR = RGBColor(38, 38, 38)  # Charcoal

# Helper Functions
def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(24)
    run.font.bold = True
    run.font.color.rgb = PRIMARY
    p.paragraph_format.space_after = Pt(4)

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(14)
    run.font.italic = True
    run.font.color.rgb = SECONDARY
    p.paragraph_format.space_after = Pt(24)

def add_heading_1(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = PRIMARY
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)

def add_heading_2(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = SECONDARY
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)

def add_paragraph(text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = TEXT_COLOR
    r_text = p.add_run(text)
    r_text.font.name = 'Calibri'
    r_text.font.size = Pt(11)
    r_text.font.color.rgb = TEXT_COLOR

def add_bullet(text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = TEXT_COLOR
    r_text = p.add_run(text)
    r_text.font.name = 'Calibri'
    r_text.font.size = Pt(11)
    r_text.font.color.rgb = TEXT_COLOR

# --- Title Header ---
add_title("Global Healthcare Analytics & Life Expectancy Predictor")
add_subtitle("End-to-End Technical Project Report & Engineering Documentation")

# --- Section 1: Executive Summary ---
add_heading_1("1. Executive Summary")
add_paragraph(
    "This project presents an enterprise-grade data engineering, machine learning, and web deployment solution designed to analyze historical global healthcare data and forecast national life expectancy metrics through 2030. What began as a static CSV data examination evolved into a fully automated pipeline capable of live API data extraction, relational database normalization, advanced feature engineering, multivariate ML regression benchmarking, and dynamic scenario modeling."
)

# --- Section 2: Technical Architecture & Stack ---
add_heading_1("2. Technical Architecture & Tech Stack")
add_bullet(" Data Ingestion: Automated World Bank API REST endpoints (JSON format).", "Python requests:")
add_bullet(" Database Engine: SQLite3 relational database (`database/healthcare.db`).", "Storage & Querying:")
add_bullet(" Processing & Modeling: Pandas, NumPy, Scikit-Learn (ExtraTreesRegressor, KNNImputer, StandardScaler).", "Machine Learning:")
add_bullet(" User Interface: Streamlit interactive web dashboard (`app.py`).", "Frontend Deployment:")
add_bullet(" Version Control: Git & GitHub repository integration.", "DevOps:")

# --- Section 3: Data Pipeline & Relational DB ---
add_heading_1("3. Data Engineering & Pipeline Evolution")
add_paragraph(
    "The primary operational shift involved replacing static CSV files with a live API pipeline. Data across 200+ countries spanning 2000 to 2023 was fetched and structured into SQLite tables."
)

# Table: Schema Definition
table = doc.add_table(rows=1, cols=3)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Database Feature Column'
hdr_cells[1].text = 'Data Type'
hdr_cells[2].text = 'Analytical Purpose / Metric'

headers = ['Database Feature Column', 'Data Type', 'Analytical Purpose / Metric']
data = [
    ['country / country_code', 'TEXT', 'Primary geographical keys'],
    ['year', 'INTEGER', 'Temporal trend indexing (2000–2023)'],
    ['life_expectancy', 'FLOAT', 'Target variable (Years)'],
    ['gdp_per_capita', 'FLOAT', 'Economic health output metric ($)'],
    ['health_expenditure', 'FLOAT', 'Healthcare expenditure per capita ($)'],
    ['physicians_per_1000', 'FLOAT', 'Doctor availability density'],
    ['hospital_beds_per_1000', 'FLOAT', 'Medical infrastructure capacity'],
    ['sanitation_access_pct', 'FLOAT', 'Hygiene & disease prevention metric (%)']
]

for row in data:
    row_cells = table.add_row().cells
    row_cells[0].text = row[0]
    row_cells[1].text = row[1]
    row_cells[2].text = row[2]

# --- Section 4: Machine Learning Tournament ---
add_heading_1("4. Machine Learning Model Tournament & Results")
add_paragraph(
    "To accurately predict life expectancy while minimizing variance, feature transformations were introduced: logarithmic scaling (`log_gdp`, `log_health`) and ratio metrics (`health_gdp_ratio`). A tournament of 7 regression models was evaluated using cross-validation."
)
add_bullet(" Benchmark Champion: Extra Trees Regressor achieved an R² score of ~0.81 with a Mean Absolute Error (MAE) of ~2.3 years.", "Winning Model:")
add_bullet(" Missing Value Strategy: KNN Imputer (k=5) replaced naive mean imputation, accurately maintaining demographic correlations across underdeveloped regions.", "Imputation Engine:")

# --- Section 5: Troubleshooting & Bug Fix Log ---
add_heading_1("5. Technical Challenges, Troubleshooting & Resolutions")

add_heading_2("Issue 1: Streamlit Command Not Recognized in Terminal")
add_bullet("Root Cause: Windows environment PATH variable omitted Python script executables.", "Description:")
add_bullet("Bypassed path verification by launching execution directly through the Python module wrapper: `python -m streamlit run app.py`.", "Resolution:")

add_heading_2("Issue 2: Static Predictions & Country Dropdown Disconnect")
add_bullet("Root Cause: Dropdown selection updated historical line plots but left prediction sliders sitting at static default parameters.", "Description:")
add_bullet("Linked country selection directly to default state of sidebar parameters, automatically auto-filling real-time metrics for selected countries.", "Resolution:")

add_heading_2("Issue 3: Decision Tree Extrapolation Boundaries (Capped at 2023)")
add_bullet("Root Cause: Tree-based models cannot extrapolate linear trends beyond maximum training ranges (2023).", "Description:")
add_bullet("Designed a dual-series plot (Blue for historical data, Red for predictive scenario) mapping future trajectories up to 2030 based on user-controlled inputs.", "Resolution:")

add_heading_2("Issue 4: Omitted Variable Bias")
add_bullet("Root Cause: Initial reliance on GDP and direct spending ignored structural sanitation and healthcare infrastructure.", "Description:")
add_bullet("Executed `notebooks/02_merge_new_data.py` to pull Hospital Beds per 1,000 and Basic Sanitation Access via World Bank API, significantly reducing bias and updating India's baseline forecast from 70.6 to 71.6 years.", "Resolution:")

add_heading_2("Issue 5: SQLite Database Locking (`no such column` errors)")
add_bullet("Root Cause: Active Streamlit server locked `healthcare.db`, preventing schema alteration scripts from completing.", "Description:")
add_bullet("Gracefully terminated active processes (`Ctrl + C`), cleared stale Streamlit resource caches (`@st.cache_resource`), and safely executed relational schema overwrite.", "Resolution:")

# --- Section 6: Summary & Impact ---
add_heading_1("6. Final Upgrades & Project Conclusion")
add_paragraph(
    "The completed project bridges the gap between raw data pipelines, machine learning benchmarking, and intuitive user interfaces. By solving key statistical anomalies (such as omitted variable bias) and technical infrastructure locks, the solution serves as an interactive decision-support tool for public policy analysis."
)

# Save Document
doc.save("Healthcare_Analytics_Project_Report.docx")
print("Report generated successfully: Healthcare_Analytics_Project_Report.docx")