import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go
import statsmodels.api as sm

# Page configuration
st.set_page_config(page_title="Gemscap Dashboard", layout="wide")
st.title("📊 Gemscap — Quant Analytics Dashboard")

# Database path
DB_PATH = "gemscap.db"

# Load data from SQLite
connection = sqlite3.connect(DB_PATH)
dataframe = pd.read_sql("SELECT * FROM ticks", connection)
connection.close()

# Convert timestamp column
dataframe["ts"] = pd.to_datetime(
    dataframe["ts"], format="mixed", utc=True
)

# Sidebar controls
available_symbols = dataframe["symbol"].unique()

symbol_1 = st.sidebar.selectbox(
    "Select Symbol 1",
    available_symbols,
    index=0
)

symbol_2 = st.sidebar.selectbox(
    "Select Symbol 2",
    available_symbols,
    index=1
)

rolling_window = st.sidebar.slider(
    "Z-Score Rolling Window",
    min_value=10,
    max_value=100,
    value=30
)

alert_threshold = st.sidebar.slider(
    "Alert Threshold",
    min_value=1.0,
    max_value=3.0,
    value=2.0,
    step=0.1
)

# Prepare price series
price_series_1 = (
    dataframe[dataframe["symbol"] == symbol_1]
    .set_index("ts")
    .resample("1T")
    .last()["price"]
)

price_series_2 = (
    dataframe[dataframe["symbol"] == symbol_2]
    .set_index("ts")
    .resample("1T")
    .last()["price"]
)

# Align both series
analysis_data = pd.concat(
    [price_series_1, price_series_2],
    axis=1
).dropna()

analysis_data.columns = ["price_1", "price_2"]

# Calculate hedge ratio using OLS
X = sm.add_constant(analysis_data["price_2"])
y = analysis_data["price_1"]

hedge_ratio = sm.OLS(y, X).fit().params["price_2"]

# Compute spread and Z-score
analysis_data["spread"] = (
    analysis_data["price_1"]
    - hedge_ratio * analysis_data["price_2"]
)

analysis_data["z_score"] = (
    analysis_data["spread"]
    - analysis_data["spread"].rolling(rolling_window).mean()
) / analysis_data["spread"].rolling(rolling_window).std()

latest_z_score = analysis_data["z_score"].iloc[-1]

# Alert logic
if abs(latest_z_score) >= alert_threshold:
    st.error(
        f"🚨 ALERT! Z-Score = {latest_z_score:.2f} "
        f"crossed threshold {alert_threshold}"
    )
else:
    st.success(
        f"✅ Z-Score within range: {latest_z_score:.2f}"
    )

# Charts layout
left_col, right_col = st.columns(2)

with left_col:
    spread_fig = go.Figure()
    spread_fig.add_trace(
        go.Scatter(
            x=analysis_data.index,
            y=analysis_data["spread"],
            mode="lines",
            name="Spread"
        )
    )
    spread_fig.update_layout(title="Spread")
    st.plotly_chart(spread_fig, use_container_width=True)

with right_col:
    zscore_fig = go.Figure()
    zscore_fig.add_trace(
        go.Scatter(
            x=analysis_data.index,
            y=analysis_data["z_score"],
            mode="lines",
            name="Z-Score"
        )
    )
    zscore_fig.add_hline(
        y=alert_threshold,
        line_dash="dash",
        line_color="red"
    )
    zscore_fig.add_hline(
        y=-alert_threshold,
        line_dash="dash",
        line_color="red"
    )
    zscore_fig.update_layout(title="Z-Score")
    st.plotly_chart(zscore_fig, use_container_width=True)

# Latest metrics section
st.subheader("📌 Latest Metrics")
st.write(f"**Hedge Ratio (Beta):** {hedge_ratio:.4f}")
st.write(f"**Latest Z-Score:** {latest_z_score:.2f}")
