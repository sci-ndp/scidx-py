# sciDXClient

A client to interact with the sciDX REST API.

## Parameters

- `api_url` (str): The base URL of the sciDX REST API.

## Attributes

- `api_url` (str): The base URL of the sciDX REST API.
- `token` (str): The authentication token. see [login](../api/login.md)

## Methods

### `__init__`

Initialize the sciDXClient with the API URL.

#### Parameters

- `api_url` (str): The base URL of the external API.

### `_get_headers`

Get the headers for the API request.

#### Returns

- `dict`: A dictionary containing the headers.

## Example

```python
from scidx.client import sciDXClient

# Initialize the client with the base URL of the sciDX REST API
client = sciDXClient(api_url="http://example.com/api")

# Set the authentication token (if applicable)
client.token = "your_auth_token"

# Get the headers for the API request
headers = client._get_headers()

print(headers)
```

Return to [Usage](../usage.md)