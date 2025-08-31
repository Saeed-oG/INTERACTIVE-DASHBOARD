# Import required libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO
import matplotlib.ticker as ticker

@st.cache_data # Cache data to reduce loading time
def load_data():
    indata = pd.read_csv('supermarket_sales - Sheet1.csv')
    indata['Date'] = pd.to_datetime(indata['Date']) # Convert 'Date' column to datetime
    indata['Month'] = indata['Date'].dt.to_period('M').astype(str) # Creat month column with YYYY-MM format
    return indata

# Set page layout to wide
st.set_page_config(layout="wide")

# Load dataset
indata = load_data()
print(indata.head())

# Dashboard title and description
st.title("Supermarket Sales Dashboard")
st.write("Interactive dashboard to analyze supermarket sales data.")

# Create two-column layout for filters and metrics
col1, col2 = st.columns(2)

with col1:
    # Interactive filters
    st.subheader("Filter Data")
    cities = st.multiselect("Select City:", options=indata['City'].unique(), default=indata['City'].unique())
    product_lines = st.multiselect("Select Product Line:", options=indata['Product line'].unique(), default=indata['Product line'].unique())
    customer_types = st.multiselect("Select Customer Type:", options=indata['Customer type'].unique(), default=indata['Customer type'].unique())

# Filter data based on selections
filtered_indata = indata[indata['City'].isin(cities) & indata['Product line'].isin(product_lines) & indata['Customer type'].isin(customer_types)]

with col2:
    # Display key metrics
    st.subheader("Key Metrics")
    total_sales = filtered_indata['Total'].sum()
    avg_sales = filtered_indata['Total'].mean()
    st.metric("Total Sales", f"${total_sales:,.2f}")
    st.metric("Average Sale", f"${avg_sales:,.2f}")

# Display filtered data table
st.subheader("Filtered Sales Data")
st.dataframe(filtered_indata.head(10))

# Download filtered data as CSV
st.subheader("Download Filtered Data")
csv = filtered_indata.to_csv(index=False, encoding='utf-8-sig')
st.download_button(
    label="📥Download CSV",
    data=csv,
   file_name=f"sales_data_{pd.Timestamp.now().strftime('%Y-%m-%d')}.csv",
    mime="text/csv"
)

# Visualizations
st.subheader("Visualizations")
col3, col4 = st.columns(2)

with col3:
    # Bar chart for sales by city
    city_sales = (filtered_indata.groupby('City')['Total'].sum()
              .reset_index()
              .sort_values('Total', ascending=True))
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(data=city_sales, x='Total', y='City', palette='viridis', ax=ax)
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    plt.title('Total Sales by City', fontsize=14, fontweight='bold')
    plt.xlabel('Total Sales', fontsize=12)
    plt.ylabel('City', fontsize=12)
    st.pyplot(fig)

with col4:
    # Bar chart for sales by product line
    product_sales = filtered_indata.groupby('Product line')['Total'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=product_sales, x='Total', y='Product line', hue='Product line', palette='Greens', ax=ax)
    plt.title('Total Sales by Product Line')
    plt.xlabel('Total Sales')
    plt.ylabel('Product Line')
    st.pyplot(fig)

# Line chart for monthly sales trend
st.subheader("Monthly Sales Trend")
monthly_sales = filtered_indata.groupby('Month')['Total'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=monthly_sales, x='Month', y='Total', marker='o', ax=ax)
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)

