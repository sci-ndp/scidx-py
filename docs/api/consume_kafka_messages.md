# consume_kafka_messages

Consume Kafka messages from a given topic using the API.

## Parameters

- `topic` (str): The Kafka topic to consume messages from.

## Returns

- `list`: A list of consumed messages.

## Raises

- `HTTPError`: If the API request fails with detailed error information.

## Example

```python
from scidx.client import sciDXClient

# Initialize the client with the base URL of the sciDX REST API
client = sciDXClient(api_url="http://example.com/api")

# Set the authentication token
client.token = "your_auth_token"

# Define the topic to consume messages from
topic = "example_topic"

# Consume Kafka messages
messages = client.consume_kafka_messages(topic)

for message in messages:
    print(message)
```

Return to [Usage](../usage.md)
    
