# create_kafka_stream

Create a new Kafka stream in the sciDX system.

## Parameters

- `keywords` (list): A list of keywords to filter the data sources.
- `filter_semantics` (dict): A dictionary containing filter semantics to apply to the streams.
- `client.token` (str): The authentication token. see [login](../api/login.md)

## Returns

- `dict`: A dictionary containing the response from the API, including the topic of the created stream.

## Raises

- `HTTPError`: If the API request fails with detailed error information.

## Example

```python
from scidx.client import sciDXClient

# Initialize the client with the base URL of the sciDX REST API
client = sciDXClient(api_url="http://example.com/api")

# Set the authentication token
client.token = "your_auth_token"

# Define the parameters for the new Kafka stream
keywords = ["data", "science"]
filter_semantics = {
    "include": ["research", "analysis"],
    "exclude": ["unrelated"]
}

# Create the Kafka stream
response = client.create_kafka_stream(keywords, filter_semantics)

print(response)