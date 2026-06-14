import time
import json
import random
from datetime import datetime


def generate_market_ticks():
    base_price = 65000.00
    print("📡 Ingestion Engine Active. Broadcasting live ticks to local storage...")

    while True:
        # Simulate market price variance
        price_change = random.normalvariate(0, 15)
        base_price = round(base_price + price_change, 2)
        timestamp = datetime.now().strftime("%H:%M:%S")

        payload = {
            "ticker": "BTC-USD",
            "price": base_price,
            "timestamp": timestamp
        }

        # Write the payload to a shared local file buffer
        with open("stream_buffer.json", "w") as f:
            json.dump(payload, f)

        print(f"✅ Broadcasted Packet: {payload}")
        time.sleep(1.0)  # Push a new update every second


if __name__ == '__main__':
    try:
        generate_market_ticks()
    except KeyboardInterrupt:
        print("\n🛑 Ingestion Engine Halted.")