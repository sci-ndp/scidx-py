## Usage

Here is a quick example of how to use the library:

```python

from scidx import sciDXClient


# Initialize the client

api_url ="http://your-api-url.com"

client = sciDXClient(api_url)


# Register an organization

response = client.register_organization(

    name="example_org",

    title="Example Organization",

    description="This is an example organization."

)

print(response)


# Register a URL resource

response = client.register_url(

    resource_name="example_resource",

    resource_title="Example Resource Title",

    owner_org="example_org",

    resource_url="http://example.com/resource",

    notes="This is a resource for testing."

)

print(response)


# Register an S3 resource

response = client.register_s3(

    resource_name="example_resource",

    resource_title="Example Resource Title",

    owner_org="example_org",

    resource_s3="s3://example-bucket/resource",

    notes="This is a resource for testing."

)

print(response)


# Search for organizations

organizations = client.search_organization()

print(organizations)


# Search for resources

resources = client.search_resource(resource_name="example_resource")

print(resources)

```

For more usage examples and detailed explanations, see [Usage](https://github.com/sci-ndp/scidx-py/blob/main/docs/usage.md).
