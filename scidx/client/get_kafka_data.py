from aiokafka import AIOKafkaConsumer
from typing import List
import asyncio

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
