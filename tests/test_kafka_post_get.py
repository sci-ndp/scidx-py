import random
import string
import json
import requests
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import asyncio
import pytest
import time

# Constants
API_URL = "http://localhost:8000"
KAFKA_HOST = '155.101.6.194'
KAFKA_PORT = '9092'
KAFKA_TOPIC_PREFIX = 'random_topic_example_'
OWNER_ORG = "deleteme_org"

# Function to generate a unique Kafka topic name
def generate_unique_kafka_topic():
    return KAFKA_TOPIC_PREFIX + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# Function to post Kafka dataset data to CKAN
def post_kafka_datasource(api_url, dataset_data):
    endpoint = f"{api_url}/kafka"
    response = requests.post(endpoint, json=dataset_data)

    if response.status_code == 201:
        print("Dataset created successfully:", response.json())
        return response.json()
    else:
        print("Error creating dataset:", response.status_code, response.json())
        response.raise_for_status()

# Kafka Producer class to send random messages
class KafkaProducer:
    def __init__(self, host, port, topic):
        self.host = host
        self.port = port
        self.topic = topic

    async def send_random_messages(self, num_messages):
        producer = AIOKafkaProducer(bootstrap_servers=f"{self.host}:{self.port}")
        await producer.start()
        try:
            for _ in range(num_messages):
                message = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
                await producer.send_and_wait(self.topic, message.encode('utf-8'))
                print(f"Sent message: {message}")
        finally:
            await producer.stop()

# Kafka Consumer function to consume messages
async def consume_kafka_messages(topic, host, port, group_id):
    consumer = AIOKafkaConsumer(
        topic,
        group_id=group_id,
        bootstrap_servers=f"{host}:{port}",
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        fetch_max_bytes=104857600,  # 100MB fetch size
        max_poll_records=1000  # Fetch up to 1000 messages per poll
    )
    await consumer.start()
    try:
        messages = []
        async for msg in consumer:
            print(f"Consumed message: {msg.value.decode('utf-8')}")
            messages.append(msg.value.decode('utf-8'))
            if len(messages) >= 10:
                break
        return messages
    finally:
        await consumer.stop()

# Function to get Kafka datasets from CKAN
def get_kafka_datasets(api_url):
    endpoint = f"{api_url}/kafka"
    response = requests.get(endpoint)
    if response.status_code == 200:
        datasets = response.json()
        return datasets
    else:
        print(f"Failed to retrieve datasets. Status code: {response.status_code}, Response: {response.text}")
        response.raise_for_status()

# Pytest test function
@pytest.mark.asyncio
async def test_kafka_ckan_integration():
    # Generate a unique Kafka topic name
    kafka_topic = generate_unique_kafka_topic()

    # Step 1: Send random messages to Kafka topic
    producer = KafkaProducer(KAFKA_HOST, KAFKA_PORT, kafka_topic)
    await producer.send_random_messages(num_messages=10)

    # Step 2: Register Kafka topic as dataset in CKAN
    dataset_data = {
        "dataset_name": kafka_topic,
        "dataset_title": "Random Topic Example",
        "owner_org": OWNER_ORG,
        "kafka_topic": kafka_topic,
        "kafka_host": KAFKA_HOST,
        "kafka_port": KAFKA_PORT,
        "dataset_description": "This is a randomly generated Kafka topic registered as a CKAN dataset."
    }
    post_kafka_datasource(API_URL, dataset_data)

    # Add a delay to ensure the dataset is indexed
    time.sleep(5)

    # Step 3: Retrieve Kafka dataset information from CKAN
    kafka_datasets = get_kafka_datasets(API_URL)
    dataset_info = next((ds for ds in kafka_datasets if ds['name'] == kafka_topic), None)
    assert dataset_info is not None

    # Step 4: Consume messages from Kafka topic using retrieved information
    resource = dataset_info['resources'][0]
    kafka_host, kafka_port, kafka_topic = resource['url'].split(';')
    messages = await consume_kafka_messages(kafka_topic, kafka_host, kafka_port, OWNER_ORG)
    print('Messages:\n', messages)
    assert len(messages) > 0

if __name__ == "__main__":
    pytest.main([__file__])
