import streamlit as st
import pandas as pd
from datetime import datetime
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

# 1. Setup layout page configurations
st.set_page_config(
    page_title="High-Frequency Financial Stream Engine",
    page_icon="📈",
    layout="wide"
)

st.title("📈 High-Frequency Financial Data Stream Engine")
st.markdown("Retrieving real-time market telemetry from cloud stream brokers and rendering chronological analytics.")

# Initialize session state cache arrays for tracking sliding chart windows
if 'chart_prices' not in st.session_state:
    st.session_state.chart_prices = []
if 'time_labels' not in st.session_state:
    st.session_state.time_labels = []

# 2. Establish layout columns for visual dashboard metric cards
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


# 3. Stream Handler Callback class to catch incoming data packets
class DashboardStreamListener(SubscribeCallback):
    def message(self, pubnub, message):
        tick_data = message.message
        current_price = tick_data['price']
        timestamp = tick_data['timestamp']

        # Append data to global runtime session cache
        st.session_state.chart_prices.append(current_price)
        st.session_state.time_labels.append(timestamp)

        # Maintain a clean 20-period sliding window size
        if len(st.session_state.chart_prices) > 20:
            st.session_state.chart_prices.pop(0)
            st.session_state.time_labels.pop(0)

        # Calculate moving window analytics
        rolling_avg = sum(st.session_state.chart_prices[-10:]) / len(st.session_state.chart_prices[-10:])

        # Determine quick alert trading breakout signals
        if current_price > rolling_avg:
            signal, alert_type = "🟢 BULLISH BREAKOUT", "success"
        else:
            signal, alert_type = "🔴 BEARISH RETRACEMENT", "warning"

        # 4. Push updates to metric blocks instantly
        live_price_box.metric(label="Live Asset Valuation (BTC-USD)", value=f"${current_price:,.2f}")
        moving_avg_box.metric(label="10-Period Rolling Window Avg", value=f"${rolling_avg:,.2f}")

        if alert_type == "success":
            alert_box.success(signal)
        else:
            alert_box.warning(signal)

        # Format metrics matrix to plot the line graph
        chart_df = pd.DataFrame({
            "Market Price": st.session_state.chart_prices
        }, index=st.session_state.time_labels)

        chart_placeholder.line_chart(chart_df)


# Initialize cloud broker network connection inside Streamlit view framework
if st.button("▶️ Establish Live Stream Connection"):
    pn_config = PNConfiguration()
    pn_config.subscribe_key = "demo"
    pn_config.user_id = "streamlit_dashboard"
    pubnub = PubNub(pn_config)

    st.toast("⚡ Connected to cloud data pipeline successfully!", icon="✅")

    # Register the callback listener to process incoming ticks infinitely
    stream_listener = DashboardStreamListener()
    pubnub.add_listener(stream_listener)
    pubnub.subscribe().channels("live-ticks").execute()