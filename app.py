import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# 1. Set up professional page layout configurations
st.set_page_config(
    page_title="High-Frequency Financial Stream Engine",
    page_icon="📈",
    layout="wide"
)

st.title("📈 High-Frequency Financial Data Stream Engine")
st.markdown("Retrieving real-time market ticks from Apache Kafka cluster and computing chronological analytics.")

# 2. Create the layout columns for our visual cards
metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    live_price_box = st.empty()  # Placeholder to update price dynamically
with metric_col2:
    moving_avg_box = st.empty()  # Placeholder to update moving average
with metric_col3:
    alert_box = st.empty()  # Placeholder for trading signals

st.markdown("---")
st.subheader("📊 Volatility Tracker (Live Window)")
chart_placeholder = st.empty()

# 3. Simulating the live frontend render pipeline loop
# (Once your Kafka consumer runs, this loop will read from the active buffer)
if st.button("▶️ Connect to Live Ingestion Stream"):
    # Mock data cache to initialize our line graph
    historical_prices = list(np.random.normal(65000, 150, size=20))

    while True:
        # Generate dynamic price updates mirroring market behavior
        latest_tick = round(historical_prices[-1] + np.random.normal(0, 45), 2)
        historical_prices.append(latest_tick)

        if len(historical_prices) > 30:
            historical_prices.pop(0)  # Maintain a sliding display window

        # Calculate moving averages on the active window
        rolling_avg = round(sum(historical_prices[-10:]) / 10, 2)

        # Determine quick alert signals based on price crossing the average
        if latest_tick > rolling_avg:
            signal, alert_type = "🟢 BULLISH BREAKOUT", "success"
        else:
            signal, alert_type = "🔴 BEARISH RETRACEMENT", "inverse"

        # 4. Stream data directly to the user interface blocks
        live_price_box.metric(label="Live Asset Valuation (BTC-USD)", value=f"${latest_tick:,}")
        moving_avg_box.metric(label="10-Period Rolling Window Avg", value=f"${rolling_avg:,}")

        if alert_type == "success":
            alert_box.success(signal)
        else:
            alert_box.warning(signal)

        # Update the line chart continuously
        chart_placeholder.line_chart(historical_prices)

        # Pause briefly to mimic a streaming ticker timeline
        time.sleep(1)