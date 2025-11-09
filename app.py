import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE SETUP ---
st.set_page_config(
    page_title="P&L Financial Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- DATA LOADING ---
@st.cache_data
def load_data(filepath):
    try:
        df = pd.read_csv(filepath, thousands=',')
        
        # --- FIX: DATA CLEANING (This is the high-value skill) ---
        # The CSV has "Sept" (4 letters) which breaks the date format.
        # We will replace it with the standard "Sep" (3 letters) *before* parsing.
        df['Order Date'] = df['Order Date'].str.replace('Sept', 'Sep')
        
        # Now we can safely parse the dates using the standard 3-letter month format
        df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%b-%y')
        
        df['Weekday'] = df['Order Date'].dt.weekday
        
        return df
        
    except FileNotFoundError:
        st.error(f"Error: The file '{filepath}' was not found. Make sure your full 'Data.csv' is in the folder.")
        return None
    except KeyError as e:
        st.error(f"Error: Missing a required column: {e}. Make sure you are using the FULL assignment 'Data.csv'.")
        return None
    except ValueError as e:
        st.error(f"DATE FORMAT ERROR: {e}. Please ensure your 'data.csv' date format matches the code.")
        return None

# Load the full assignment data file
# Make sure your *full 4,000-row* assignment file is in this folder
# and is named "data.csv"
df = load_data('data.csv')

if df is not None:

    # --- SCENARIO MANAGER (This is Q6) ---
    st.sidebar.header("📈 Scenario Manager (Q6)")
    st.sidebar.markdown("Adjust the key assumptions to see the P&L impact.")
    
    selling_exp_rate = st.sidebar.slider(
        "Selling Expense Rate (%)", 
        min_value=4.0, max_value=8.0, value=5.0, step=0.5
    ) / 100
    
    admin_exp_rate = st.sidebar.slider(
        "Admin Expense Rate (% of GP)", 
        min_value=15.0, max_value=25.0, value=20.0, step=0.5
    ) / 100
    
    tax_rate = st.sidebar.slider(
        "Taxation Rate (%)", 
        min_value=30.0, max_value=50.0, value=40.0, step=0.5
    ) / 100

    # --- P&L CALCULATIONS (This is Q5) ---
    st.title("📈 P&L Financial Model Dashboard")
    st.markdown("This dashboard models a P&L statement from raw sales data and includes a 'What-If' Scenario Manager.")

    total_sales = df['Sales'].sum()
    friday_sales = df[df['Weekday'] == 4]['Sales'].sum() # 4 = Friday
    discount = friday_sales * 0.02
    net_sales = total_sales - discount
    cogs = df['Cost'].sum()
    gross_profit = net_sales - cogs
    
    commission_df = df[
        (df['Product Category'] == 'Bags') &
        (df['Brand'] == 'Callaway') &
        (df['City'].isin(['Karachi', 'Lahore', 'Islamabad']))
    ]
    commission = commission_df['Sales'].sum() * 0.05
    
    selling_expenses = total_sales * selling_exp_rate
    admin_expenses = gross_profit * admin_exp_rate
    total_op_ex = selling_expenses + commission + admin_expenses
    profit_before_tax = gross_profit - total_op_ex
    tax = profit_before_tax * tax_rate
    net_profit = profit_before_tax - tax

    # --- DISPLAY P&L AND KPIs ---
    
    st.header("Profit & Loss Statement")
    
    pnl_data = {
        "Metric": [
            "Total Sales", "Less: Friday Discount (2%)", "**Net Sales**",
            "Less: Cost of Goods Sold (COGS)", "**Gross Profit**",
            "Less: Operating Expenses", "   - Selling Expenses (from rate)", "   - Special Commissions (Q5d)",
            "   - Admin Expenses (from rate)", "**Profit Before Tax**",
            "Less: Taxation (from rate)", "**NET PROFIT (After Tax)**"
        ],
        "Value (PKR)": [
            total_sales, -discount, net_sales,
            -cogs, gross_profit,
            None, -selling_expenses, -commission,
            -admin_expenses, profit_before_tax,
            -tax, net_profit
        ]
    }
    pnl_df = pd.DataFrame(pnl_data)
    
    # Use 'width="stretch"' to remove the deprecation warning
    st.dataframe(
        pnl_df.style.format(
            {"Value (PKR)": "{:,.0f}"}, na_rep=""
        ).apply(
            lambda x: ['font-weight: bold' if "bold" in str(v) else '' for v in x], 
            axis=1
        ),
        width='stretch', # Replaced use_container_width=True
        hide_index=True
    )

    st.markdown("---")
    st.header("Profitability KPIs")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Gross Profit Margin", f"{gross_profit / net_sales:.1%}")
    col2.metric("Operating Margin", f"{profit_before_tax / net_sales:.1%}")
    col3.metric("Net Profit Margin", f"{net_profit / net_sales:.1%}")
    
    # --- VISUALIZATIONS ---
    st.markdown("---")
    st.header("Visual Analysis")
    
    st.subheader("Profit Waterfall")
    
    # Fixed the iloc indices to account for the dropped None row
    plot_df = pnl_df.dropna().iloc[[2, 4, 8, 10]] 
    
    waterfall_fig = px.bar(
        plot_df, 
        x="Metric", y="Value (PKR)", 
        title="Profitability Breakdown",
        color="Metric",
        text_auto=".2s"
    )
    waterfall_fig.update_layout(showlegend=False)
    st.plotly_chart(waterfall_fig, use_container_width=True) 

else:
    st.warning("Data file not loaded. Make sure the *full* 'data.csv' file is in the project folder and the date format is correct.")