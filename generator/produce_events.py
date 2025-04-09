import json
import random
import time
import uuid
from datetime import datetime
from kafka import KafkaProducer

# Kafka setup
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Configuration
categories = ["sports", "politics", "tech", "finance", "entertainment"]
devices = ["mobile", "desktop", "tablet"]
countries = [
    "Argentina", "Brazil", "Canada", "Germany", "Japan", "Spain",
    "USA", "India", "France", "Australia", "UK"
]

# Generate fixed UUID article IDs per category
def generate_articles():
    return [str(uuid.uuid4()) for _ in range(20)]

articles_per_category = {cat: generate_articles() for cat in categories}

# Simulate breaking news on one finance article
breaking_article = random.choice(articles_per_category["finance"])

# Print mapping (optional)
print("Breaking article (finance):", breaking_article)

# Simulate regular users and bot users
regular_users = [f"user_{i}" for i in range(100)]
bot_users = [f"bot_user_{i}" for i in range(3)]

def create_event(user_id=None, is_bot=False):
    category = random.choices(categories, weights=[1, 1, 1, 2, 1])[0]  # Finance slightly favored

    # Breaking news spike
    if random.random() < 0.1:
        article_id = breaking_article
        category = "finance"
    else:
        article_id = random.choice(articles_per_category[category])

    device = random.choice(devices)
    country = random.choice(countries)
    session_id = str(uuid.uuid4()) if not is_bot else f"bot_session_{user_id}"

    return {
        "user_id": user_id if user_id else random.choice(regular_users),
        "article_id": article_id,
        "timestamp": datetime.utcnow().isoformat(),
        "category": category,
        "location": country,
        "device_type": device,
        "session_id": session_id
    }

def send_events():
    while True:
        events = []

        # Normal traffic
        for _ in range(10):
            events.append(create_event())

        # Finance-engaged users
        for _ in range(5):
            events.append(create_event(user_id=random.choice(regular_users)))

        # Bot traffic (burst mode)
        for bot_id in bot_users:
            for _ in range(random.randint(5, 10)):
                events.append(create_event(user_id=bot_id, is_bot=True))

        # Send all events
        for event in events:
            producer.send('news_events', event)

        producer.flush()
        print(f"[{datetime.utcnow().isoformat()}] Sent {len(events)} events")
        time.sleep(1)  # New batch every second

if __name__ == "__main__":
    send_events()
