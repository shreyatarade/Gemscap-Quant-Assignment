# Gemscap-Quant-Assignment
Quantitative analytics dashboard for pair trading using Python and Streamlit
# 📊 Gemscape — Quant Analytics Dashboard

**Quantitative analytics dashboard for pair trading using Python and Streamlit**

## 📝 Description

Gemscape Dashboard is a **real-time quantitative trading analytics tool** built with Python. It allows you to:

- Analyze **pair trading opportunities** between two symbols.
- Calculate **hedge ratios** using OLS regression.
- Compute **spread** and **Z-Score** to detect market anomalies.
- Get **alerts** when Z-Score crosses a threshold.
- Visualize **spread** and **Z-Score** trends interactively.

This dashboard is perfect for **quant analysts, traders, and students** who want to explore statistical arbitrage strategies.


## ⚙️ Features

- Select **any two symbols** from your dataset
- Calculate **hedge ratio (beta)** dynamically
- Compute **spread** and **rolling Z-Score**
- Set **custom rolling window** and **alert thresholds**
- **Interactive Plotly charts** for spread and Z-Score
- Real-time **alerts** for trading signals


## 🛠 Technologies Used

- **Python 3.10+**  
- **Streamlit** — Interactive web dashboard  
- **Pandas** — Data manipulation  
- **SQLite3** — Database for storing tick data  
- **Plotly** — Interactive visualizations  
- **Statsmodels** — Statistical modeling (OLS regression)  


## 📂 Repository Structure
Gemscap-Quant-Assignment/
│
├── dashboard.py # Main Streamlit dashboard code
├── gemscape.db # SQLite database with tick data
├── requirements.txt # Python dependencies
├── README.md # This file
└── sample_data/ # (Optional) example CSV files if needed


## 🚀 Installation & Setup

Clone the repository: git clone https://github.com/your-username/Gemscap-Quant-Assignment.git
cd Gemscap-Quant-Assignment
Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate (Linux / Mac)
venv\Scripts\activate (Windows)
Install dependencies: pip install -r requirements.txt
Run the dashboard: streamlit run dashboard.py
Open the browser at http://localhost:8501
 to view the dashboard


## Usage:

Select two symbols from the sidebar dropdown
Set rolling window (minutes) for Z-Score calculation
Set alert threshold for trading signals
View Spread and Z-Score charts
Check latest metrics (hedge ratio and Z-Score) at the bottom
Alert will appear if Z-Score exceeds the set threshold


## Notes:
Ensure your gemscape.db database has a ticks table with columns: ts (Timestamp), symbol (Symbol name), price (Tick price)
Data must be continuous for accurate resampling and Z-Score calculation


## Contributors:

Shreya Tarade — Project Lead & Developer


## References:

Pandas Documentation — https://pandas.pydata.org
Streamlit Documentation — https://streamlit.io
Statsmodels OLS Regression — https://www.statsmodels.org
Plotly Python Graphing — https://plotly.com/python/


## License:
This project is open source and free to use for educational purposes.

