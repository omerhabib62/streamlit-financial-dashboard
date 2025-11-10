# P&L Financial Model Dashboard

🔴 This is a Streamlit-powered P&L (Profit & Loss) Financial Model Dashboard that transforms raw sales data into actionable financial insights.

## 1. Project Overview

This is an advanced financial analysis project that demonstrates expertise in data cleaning, financial modeling, and interactive dashboard creation.

The dashboard automatically processes raw sales data, calculates key financial metrics (like Gross Profit, Operating Expenses, and Net Profit), and provides an interactive "What-If" Scenario Manager for financial planning and analysis.

This tool could be valuable for financial analysts, business managers, or anyone needing to model P&L statements from raw sales data.

## 2. Features

💼 **P&L Statement Generator:** Automatically builds a full P&L from raw sales data.

📊 **Scenario Manager:** Interactive sliders for:
- Selling Expense Rate (4-8%)
- Admin Expense Rate (15-25% of GP)
- Taxation Rate (30-50%)

📈 **KPI Dashboard:** Shows key metrics:
- Gross Profit Margin
- Operating Margin
- Net Profit Margin

📉 **Profit Waterfall:** Interactive Plotly visualization showing profit breakdown.

🧮 **Smart Data Cleaning:** Handles common date format issues (e.g., "Sept" vs "Sep").

## 3. Tech Stack

This project showcases expertise in:

**Python:** Core business logic and calculations.

**Pandas:** For data manipulation and financial computations.

**Streamlit:** Powers the interactive web interface.

**Plotly:** Creates the waterfall visualization.

## 4. How to Run Locally

1. Clone this repository:
```powershell
git clone [YOUR_REPO_URL]
```

2. Navigate to the folder:
```powershell
cd financial-dashboard
```

3. Create and activate virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:
```powershell
pip install -r requirements.txt
```

5. Ensure your `data.csv` is in the project root (must have these columns):
   - Order Date
   - Sales
   - Cost
   - Product Category
   - Brand
   - City

6. Run the app:
```powershell
streamlit run app.py
```

## 5. Data Requirements

The app expects a `data.csv` file with:

**Required Columns:**
- Order Date (format: DD-MMM-YY)
- Sales (numeric)
- Cost (numeric)
- Product Category (string)
- Brand (string)
- City (string)

**Date Format:**
- Uses DD-MMM-YY (e.g., "15-Sep-23")
- Auto-fixes "Sept" to "Sep"

## 6. Error Handling

The app includes robust error handling for:
- Missing data file
- Missing required columns
- Date format issues
- Invalid data types

Each error produces a clear, user-friendly message explaining the issue and how to fix it.

## 7. Development Notes

**Caching:**
- Uses `@st.cache_data` for efficient data loading
- Prevents redundant CSV reads

**Performance:**
- Optimized date parsing
- Efficient financial calculations
- Responsive UI updates

**Future Enhancements:**
- Export functionality (CSV/PDF)
- Unit tests for calculations
- Docker containerization
- CI/CD pipeline
- Multiple data source support
