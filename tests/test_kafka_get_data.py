import pytest
import asyncio
from scidx.client.kafka_client import KafkaClient
from scidx.client.get_kafka_data import consume_kafka_messages

# Constants
API_URL = "http://localhost:8000"
KAFKA_HOST = '155.101.6.194'
KAFKA_PORT = '9092'
KAFKA_TOPIC = 'consumer_wind-w067'

@pytest.fixture
def kafka_client():
    return KafkaClient(API_URL)

@pytest.mark.asyncio
async def test_kafka_get_and_consume(kafka_client):
    # Step 1: Retrieve Kafka dataset information from API
    kafka_datasets = kafka_client.search_kafka(kafka_topic=KAFKA_TOPIC, kafka_host=KAFKA_HOST, kafka_port=KAFKA_PORT)

    # Ensure that at least one dataset is returned
    assert len(kafka_datasets) > 0, "No Kafka datasets found"

    dataset_info = next((ds for ds in kafka_datasets if ds['resources'][0]['kafka_topic'] == KAFKA_TOPIC), None)
    assert dataset_info is not None, f"Kafka topic {KAFKA_TOPIC} not found in datasets"

    # Step 2: Consume messages from Kafka topic using retrieved information
    resource = dataset_info['resources'][0]
    kafka_host = resource['kafka_host']
    kafka_port = resource['kafka_port']
    kafka_topic = resource['kafka_topic']

    print(f"Starting to consume messages from topic: {kafka_topic}")
    messages_task = asyncio.create_task(consume_kafka_messages(
        topic=kafka_topic,
        host=kafka_host,
        port=kafka_port
    ))

    try:
        await asyncio.sleep(30)
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
