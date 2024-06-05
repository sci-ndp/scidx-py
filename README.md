# scidx

scidx is a Python library designed to interact with the sciDX REST API, allowing users to create and manage datasets easily.

## Installation

```bash
pip install scidx
```

## Usage

### Initializing the Client

```python
from scidx.client import sciDXClient

# Initialize the client with the base URL of the sciDX REST API
client = sciDXClient(api_url="http://example.com/api")
```

### Creating a Data Source

```python
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
## Contributing

1. Fork the repository.
2. Create a new branch (git checkout -b feat/new-feature).
3. Commit your changes (git commit -am 'feat: Add new feature').
4. Push the branch (git push origin feat/new-feature).
5. Open a Pull Request.

## License

This project is licensed under the [Apache License](LICENSE) - see the LICENSE file for details.
