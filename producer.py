import time
import json
import random
from datetime import datetime
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

# 1. Configure the cloud stream broker
pn_config = PNConfiguration()
pn_config.subscribe_key = "demo"  # Public demo keys provided by PubNub
pn_config.publish_key = "demo"
pn_config.user_id = "financial_producer"
pubnub = PubNub(pn_config)


def generate_market_ticks():
    """Simulates high-frequency asset price movements."""
    base_price = 65000.00
    print("📡 Cloud Ingestion Engine Active. Broadcasting live ticks to 'live-ticks' channel...")

    while True:
        # Simulate high-frequency market variance
        price_change = random.normalvariate(0, 15)
        base_price = round(base_price + price_change, 2)

        payload = {
            "ticker": "BTC-USD",
            "price": base_price,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }

        # Publish directly to the cloud streaming infrastructure
        pubnub.publish().channel("live-ticks").message(payload).sync()
        print(f"✅ Broadcasted Packet: {payload}")

        time.sleep(1.5)  # Stream an update every 1.5 seconds


if __name__ == '__main__':
    try:
        generate_market_ticks()
    except KeyboardInterrupt:
        print("\n🛑 Ingestion Engine Halted.")