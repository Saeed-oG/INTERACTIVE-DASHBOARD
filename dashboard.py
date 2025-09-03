import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------
# Page Config (must be first after imports)
# ----------------------
st.set_page_config(page_title="Supermarket Dashboard", layout="wide")

# ----------------------
# Authentication System
# ----------------------

# Initialize login state if not exists
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# Hardcoded users (username: password)
users = {
    "admin": "1234",
    "ali": "pass123",
    "maryam": "mypassword"
}

# If not logged in → Show login form
if not st.session_state.logged_in:
    st.sidebar.subheader("Hello Everyone<3")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.show_welcome = True
            st.rerun()  # refresh after login
        else:
            st.error("Invalid username or password")
    st.stop()

# If logged in → Show logout button
st.sidebar.write(f"Logged in as: {st.session_state.username}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# Show welcome message only once after login
if st.session_state.show_welcome:
    st.success(f"Welcome {st.session_state.username}!")
    st.session_state.show_welcome = False

# ----------------------
# Theme Toggle
# ----------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

if st.sidebar.button("Toggle Theme"):
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
    st.rerun()

# Apply custom CSS based on theme
if st.session_state.theme == "dark":
    st.markdown(
        """
        <style>
        body {background-color: #0E1117; color: #FAFAFA;}
        .stApp {background-color: #0E1117; color: #FAFAFA;}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        body {background-color: #FFFFFF; color: #000000;}
        .stApp {background-color: #FFFFFF; color: #000000;}
        </style>
        """,
        unsafe_allow_html=True
    )


# ----------------------
# Load Data
# ----------------------
@st.cache_data
def load_data():
    indata = pd.read_csv('supermarket_sales - Sheet1.csv')
    indata['Date'] = pd.to_datetime(indata['Date'])
    indata['Month'] = indata['Date'].dt.to_period('M').astype(str)
    return indata

indata = load_data()

# ----------------------
# Dashboard Content
# ----------------------
st.title("Supermarket Sales Dashboard")
st.write("Interactive dashboard to analyze supermarket sales data.")

# Two-column layout for filters and metrics
col1, col2 = st.columns(2)

with col1:
    # Interactive filters
    st.subheader("Filter Data")
    cities = st.multiselect("Select City", options=indata['City'].unique(), default=indata['City'].unique())
    product_lines = st.multiselect("Select Product Line", options=indata['Product line'].unique(), default=indata['Product line'].unique())
    customer_types = st.multiselect("Select Customer Type", options=indata['Customer type'].unique(), default=indata['Customer type'].unique())

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

# Download filtered data
st.subheader("Download Filtered Data")
csv = filtered_indata.to_csv(index=False, encoding='utf-8-sig')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv"
)

# ----------------------
# Visualizations
# ----------------------
st.subheader("Visualizations")
col3, col4 = st.columns(2)

with col3:
    # Bar chart for sales by city
    city_sales = filtered_indata.groupby('City')['Total'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(data=city_sales, x='Total', y='City', hue='City', palette='Blues', ax=ax)
    plt.title('Total Sales by City')
    plt.xlabel('Total Sales')
    plt.ylabel('City')
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
fig, ax = plt.subplots(figsize=(8, 4))
sns.lineplot(data=monthly_sales, x='Month', y='Total', marker='o', ax=ax)
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(fig)

