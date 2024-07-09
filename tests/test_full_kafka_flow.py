import pytest
import asyncio
import random
import string
import time
from aiokafka import AIOKafkaProducer
from scidx.client import sciDXClient
from aiokafka import AIOKafkaConsumer
from typing import List

# Constants
API_URL = "http://localhost:8000"
KAFKA_HOST = '155.101.6.194'
KAFKA_PORT = '9092'
KAFKA_TOPIC_PREFIX = 'random_topic_example_'
OWNER_ORG = "test_org4"
USERNAME = "placeholder@placeholder.com"
PASSWORD = "placeholder"

async def consume_kafka_messages(topic: str, host: str, port: str) -> List[str]:
    """
    Consume messages from a Kafka topic indefinitely until interrupted.

    Parameters
    ----------
    topic : str
        The Kafka topic name.
    host : str
        The Kafka host.
    port : str
        The Kafka port.

    Returns
    -------
    List[str]
        A list of consumed messages.
    """
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=f"{host}:{port}",
        auto_offset_reset='earliest',
        enable_auto_commit=False,
        fetch_max_bytes=104857600,  # 100MB fetch size
        max_poll_records=1000  # Fetch up to 1000 messages per poll
    )
    await consumer.start()
    messages = []
    try:
        async for msg in consumer:
            messages.append(msg.value.decode('utf-8'))
            await asyncio.sleep(0)  # Allow other tasks to run
    except asyncio.CancelledError:
        print("Consumption cancelled. Cleaning up...")
    finally:
        await consumer.stop()
        return messages

# Function to generate a unique Kafka topic name
def generate_unique_kafka_topic():
    return KAFKA_TOPIC_PREFIX + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

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

@pytest.fixture
def kafka_client():
    client = sciDXClient(API_URL)
    client.login(USERNAME, PASSWORD)
    return client

@pytest.mark.asyncio
async def test_kafka_full_flow(kafka_client):
    # Step 1: Generate a unique Kafka topic name
    kafka_topic = generate_unique_kafka_topic()

    # Step 2: Send random messages to Kafka topic
    producer = KafkaProducer(KAFKA_HOST, KAFKA_PORT, kafka_topic)
    await producer.send_random_messages(num_messages=10)

    # Step 3: Register Kafka topic as dataset
    dataset_data = {
        "dataset_name": kafka_topic,
        "dataset_title": "Random Topic Example",
        "owner_org": OWNER_ORG,
        "kafka_topic": kafka_topic,
        "kafka_host": KAFKA_HOST,
        "kafka_port": KAFKA_PORT,
        "dataset_description": "This is a randomly generated Kafka topic registered as a CKAN dataset.",
        "extras": {"key1": "value1", "key2": "value2"}  # Including extras
    }
    kafka_client.register_kafka(**dataset_data)

    # Add a delay to ensure the dataset is indexed
    time.sleep(2)

    # Step 4: Retrieve Kafka dataset information from API
    kafka_datasets = kafka_client.search_resource(
        resource_name=kafka_topic,
        resource_format="kafka"
    )

    # Ensure that at least one dataset is returned
    assert len(kafka_datasets) > 0, "No Kafka datasets found"

    dataset_info = next((ds for ds in kafka_datasets if ds['resources'][0]['name'] == kafka_topic), None)
    assert dataset_info is not None, f"Kafka topic {kafka_topic} not found in datasets"

    # Step 5: Consume messages from Kafka topic using retrieved information
    extras = dataset_info['extras']
    kafka_host = extras['host']
    kafka_port = extras['port']
    kafka_topic = extras['topic']

    print(f"Starting to consume messages from topic: {kafka_topic}")
    messages_task = asyncio.create_task(consume_kafka_messages(
        topic=kafka_topic,
        host=kafka_host,
        port=kafka_port
    ))

    try:
        await asyncio.sleep(2)
    except asyncio.CancelledError:
        pass
    finally:
        messages_task.cancel()

    try:
        messages = await messages_task
    except asyncio.CancelledError:
        messages = await messages_task

    assert len(messages) > 0, f"No messages received from topic {kafka_topic}"
    print(f"Messages from topic {kafka_topic}:\n")
    for message in messages:
        print(message)

if __name__ == "__main__":
    pytest.main([__file__])
