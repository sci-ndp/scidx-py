# create_datasource

Create a new data source in the sciDX system.

## Parameters

- `dataset_name` (str): The name of the dataset.
- `dataset_title` (str): The title of the dataset.
- `organization_id` (str): The ID of the organization.
- `resource_url` (str): The URL of the resource.
- `resource_name` (str): The name of the resource.
- `dataset_description` (str): The description of the dataset.
- `resource_description` (str): The description of the resource.
- `resource_format` (str): The format of the resource.

## Returns

- `str`: The ID of the created dataset.

## Raises

- `Exception`: If there is an error creating the dataset.

## Example

```python
from scidx.client import sciDXClient

# Initialize the client with the base URL of the sciDX REST API
client = sciDXClient(api_url="http://example.com/api")

# Define the parameters for the new data source
dataset_name = "test_dataset"
dataset_title = "Test Dataset"
organization_id = "org123"
resource_url = "http://example.com/resource"
resource_name = "Test Resource"
dataset_description = "A test dataset"
resource_description = "A test resource"
resource_format = "csv"

# Create the data source
dataset_id = client.create_datasource(
    dataset_name=dataset_name,
    dataset_title=dataset_title,
    organization_id=organization_id,
    resource_url=resource_url,
    resource_name=resource_name,
    dataset_description=dataset_description,
    resource_description=resource_description,
    resource_format=resource_format
)

print(f"Dataset created with ID: {dataset_id}")
```

Return to [client](../client.md)
