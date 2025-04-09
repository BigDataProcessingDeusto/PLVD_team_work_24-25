import json
import time
import random
from faker import Faker
from kafka import KafkaProducer
import uuid

faker = Faker()

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Predefined values
categories = ["tech", "sports", "politics", "entertainment", "finance"]
device_types = ["mobile", "desktop", "tablet"]

NUM_ARTICLES = 100
NUM_USERS = 500

# Articles with categories
articles = [
    {"article_id": uuid.uuid4(), "category": random.choice(categories)}
    for _ in range(NUM_ARTICLES)
]

# Choose a 'breaking news' article
breaking_article = random.choice(articles)
print(f"🚨 Breaking article ID: {breaking_article['article_id']} (category: {breaking_article['category']})")

# Zipf-like weight for non-breaking articles
article_weights = [NUM_ARTICLES - i for i in range(NUM_ARTICLES)]

# User pool with session tracking
users = {}
for _ in range(NUM_USERS):
    uid = uuid.uuid4()
    users[str(uid)] = {
        "session_id": str(uuid.uuid4()),
        "session_events": 0
    }

# Event loop
event_count = 0
while True:
    user_id = random.choice(list(users.keys()))
    user_info = users[user_id]

    # Session rotation
    if user_info["session_events"] >= 10:
        user_info["session_id"] = str(uuid.uuid4())
        user_info["session_events"] = 0
    user_info["session_events"] += 1

    # Random device and city
    device = random.choice(device_types)
    city = faker.city()

    # 30% chance to pick breaking article
    if random.random() < 0.3:
        article = breaking_article
    else:
        article = random.choices(articles, weights=article_weights)[0]

    event = {
        "user_id": user_id,
        "session_id": user_info["session_id"],
        "article_id": str(article["article_id"]),
        "category": article["category"],
        "location": city,
        "device_type": device,
        "timestamp": int(time.time())
    }

    producer.send("news_clicks", value=event)
    event_count += 1

    # Print every 10 events
    if event_count % 10 == 0:
        print(f"Produced event #{event_count}: {event}")

    # Simulate bursty activity
    time.sleep(random.uniform(0.2, 2.0))
