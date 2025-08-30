# INTERACTIVE-DASHBOARD

Supermarket Sales Dashboard
This project creates an interactive web dashboard to analyze supermarket sales data using Streamlit, enabling users to filter and visualize sales by city, product line, and customer type.

Project Overview
The dashboard allows users to:
- Filter sales data by city (e.g., Yangon, Mandalay), product line (e.g., Food and beverages), and customer type (Member/Normal).
- View key metrics such as total sales and average sale per transaction.
- Explore visualizations including bar charts for sales by city and product line, and a line chart for monthly sales trends.
- Download filtered data as a CSV file.
Steps
1. Setup: Loaded the supermarket sales dataset and installed Streamlit and required dependencies.
2. Data Processing: Implemented filters for city, product line, and customer type, with datetime conversion for monthly analysis.
3. Visualization: Created interactive bar charts (sales by city and product line) and a line chart (monthly sales trend).
4. Features: Added key metrics (total and average sales) and a download button for filtered data.
Tools
- Python Libraries: Streamlit, Pandas, Seaborn, Matplotlib
- Dataset: `supermarket_sales.csv` (sourced from [Kaggle](https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales))
Outputs
- dashboard.py: Dashboard source code
- supermarket_sales.csv: Sales dataset
- dashboard_screenshot.png: Screenshot of the interactive dashboard
- filtered_sales.csv: Example of downloadable filtered data
How to Run
1. Set up environment:
   - Ensure Python 3.6+ is installed.
   - Install dependencies: pip install streamlit pandas seaborn matplotlib
2. Run code: 
   - Execute ‘python -m streamlit run dashboard.py’ command in terminal
3. View dashboard: 
   - Open the provided URL (usually http://localhost:8501) in a browser.
Sample Output
“dashboard1.png, dashboard2.png and dashboard3.png” screenshots show the interactive dashboard with filters, key metrics, and visualizations.
Challenges and Solutions
-Issue: Blocking entry to interactive window when running dashboard.py in VS Code. 
-Solution: Ensured Streamlit was installed with pip install streamlit and used python -m streamlit run dashboard.py command to run in the correct Python environment.
