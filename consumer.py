import sys
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

# 1. Configure the cloud stream broker connection
pn_config = PNConfiguration()
pn_config.subscribe_key = "demo"
pn_config.user_id = "financial_consumer"
pubnub = PubNub(pn_config)

# Local cache memory to hold sliding window price metrics
price_history = []


class StreamAnalyticsEngine(SubscribeCallback):
    def message(self, pubnub, message):
        global price_history

        tick_data = message.message
        current_price = tick_data['price']
        timestamp = tick_data['timestamp']

        # Track historical prices for window calculations
        price_history.append(current_price)
        if len(price_history) > 10:
            price_history.pop(0)  # Maintain sliding time window

        # Compute chronological moving average
        rolling_avg = sum(price_history) / len(price_history)

        print(f"[{timestamp}] Price: ${current_price:<8} | 10-Tick Moving Avg: ${round(rolling_avg, 2)}")


print("📈 Analytics Engine Active. Syncing with cloud broker pipeline...")
analytics_callback = StreamAnalyticsEngine()
pubnub.add_listener(analytics_callback)
pubnub.subscribe().channels("live-ticks").execute()