import json
import time
from faker import Faker
from kafka import KafkaProducer
import random

faker = Faker()

producer = KafkaProducer(
    bootstrap_servers="kafka:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

categories = ["tech", "sports", "politics", "entertainment", "finance"]

while True:
    event = {
        "user_id": faker.uuid4(),
        "article_id": faker.uuid4(),
        "category": random.choice(categories),
        "timestamp": int(time.time())
    }
    producer.send("news_clicks", value=event)
    print("Produced:", event)
    time.sleep(1)
