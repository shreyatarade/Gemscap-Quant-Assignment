import pandas as pd
import sqlite3

# Database path
DB_PATH = "gemscap.db"

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)

# Read tick data
df = pd.read_sql("SELECT * FROM ticks", conn)

# Convert timestamp column to datetime
df["ts"] = pd.to_datetime(df["ts"], format="mixed", utc=True)
df.set_index("ts", inplace=True)

# Select two symbols for analysis
symbols = df["symbol"].unique()
symbol_1 = symbols[0]
symbol_2 = symbols[1]

# Resample prices to 1-minute frequency
price_1 = (
    df[df["symbol"] == symbol_1]
    .resample("1T")
    .last()["price"]
)

price_2 = (
    df[df["symbol"] == symbol_2]
    .resample("1T")
    .last()["price"]
)

# Combine and align both price series
combined_data = pd.concat([price_1, price_2], axis=1).dropna()
combined_data.columns = ["price_1", "price_2"]

# Calculate rolling correlation
rolling_window = 20  # minutes
combined_data["rolling_correlation"] = (
    combined_data["price_1"]
    .rolling(rolling_window)
    .corr(combined_data["price_2"])
)

# Display latest results
print("Gemscap Rolling Correlation Analysis")
print("-----------------------------------")
print(f"Symbol 1: {symbol_1}")
print(f"Symbol 2: {symbol_2}")
print(f"Rolling Window: {rolling_window} minutes")
print(f"Latest Rolling Correlation: {combined_data['rolling_correlation'].iloc[-1]:.4f}")

# Close database connection
conn.close()
