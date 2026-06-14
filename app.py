import streamlit as st
import pandas as pd
import json
import time
import os

# 1. Page Configuration
st.set_page_config(
    page_title="High-Frequency Financial Stream Engine",
    page_icon="📈",
    layout="wide"
)

st.title("📈 High-Frequency Financial Data Stream Engine")
st.markdown("Connected Architecture: Actively consuming metrics from the live Producer pipeline stream.")

# 2. Design Layout Cards
metric_col1, metric_col2, metric_col3 = st.columns(3)
with metric_col1:
    live_price_box = st.empty()
with metric_col2:
    moving_avg_box = st.empty()
with metric_col3:
    alert_box = st.empty()

st.markdown("---")
st.subheader("📊 Volatility Tracker (Live Window)")
chart_placeholder = st.empty()

# Initialize data arrays in session memory
if 'prices' not in st.session_state:
    st.session_state.prices = []
if 'timestamps' not in st.session_state:
    st.session_state.timestamps = []

# 3. Connect Button
if st.button("▶️ Connect to Live Ingestion Stream"):
    st.toast("⚡ Successfully connected to the producer stream buffer!", icon="🔌")

    status_text = st.empty()

    # 4. Continuous Consumer Processing Loop
    while True:
        status_text.caption("🔍 Consumer active: Reading packets from stream buffer...")

        # Check if the producer has generated the file yet
        if os.path.exists("stream_buffer.json"):
            try:
                # Read the latest tick data written by the producer
                with open("stream_buffer.json", "r") as f:
                    latest_packet = json.load(f)

                current_price = latest_packet['price']
                timestamp = latest_packet['timestamp']

                # Only update if it's a completely new tick timestamp
                if not st.session_state.timestamps or st.session_state.timestamps[-1] != timestamp:
                    st.session_state.prices.append(current_price)
                    st.session_state.timestamps.append(timestamp)

                    # Keep a neat 20-period viewing frame window
                    if len(st.session_state.prices) > 20:
                        st.session_state.prices.pop(0)
                        st.session_state.timestamps.pop(0)

                    # Compute rolling averages (Analytical Consumer Layer)
                    recent_window = st.session_state.prices[-10:]
                    rolling_avg = round(sum(recent_window) / len(recent_window), 2)

                    # Update metrics display objects instantly
                    live_price_box.metric(label="Live Asset Valuation (BTC-USD)", value=f"${current_price:,.2f}")
                    moving_avg_box.metric(label="10-Period Rolling Window Avg", value=f"${rolling_avg:,.2f}")

                    if current_price > rolling_avg:
                        alert_box.success("🟢 BULLISH BREAKOUT")
                    else:
                        alert_box.warning("🔴 BEARISH RETRACEMENT")

                    # Re-plot the dataframe to update the chart lines
                    chart_df = pd.DataFrame({"Market Price": st.session_state.prices},
                                            index=st.session_state.timestamps)
                    chart_placeholder.line_chart(chart_df)

            except Exception as e:
                # Handle temporary file read collisions gracefully
                pass

        time.sleep(0.5)  # Scan the buffer frequently for snappy updates