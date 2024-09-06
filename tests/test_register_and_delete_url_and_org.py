import pytest
import string
import random
from scidx.client import sciDXClient
from scidx.client import StreamProcessing, CSVProcessing, JSONProcessing

# Helper function to generate a random string
def generate_random_string(length=8):
    """
    Generate a random string of fixed length.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Test for registering and deleting multiple types of URL datasets
def test_register_and_delete_url_datasets_with_different_processing():
    """
    Test the ability to create and then delete URL datasets with
    StreamProcessing, CSVProcessing, and JSONProcessing, along with 
    their associated organization, using the real API.
    """
    # Create a client instance with the actual API URL
    client = sciDXClient(api_url="http://localhost:8765")
    
    # Set the token for authentication
    client.token = "test"
    
    # Step 1: Create a random organization
    org_name = generate_random_string()
    org_title = f"Title for {org_name}"
    org_description = "This is a test organization created for testing."

    # Register a new organization
    response_create_org = client.register_organization(
        name=org_name,
        title=org_title,
        description=org_description
    )
    
    # Check if the organization was created successfully
    assert "id" in response_create_org
    assert response_create_org.get("id") is not None  # Ensure an ID is returned
    
    # Extract the organization ID
    owner_org = response_create_org.get("id")

    # Define the dataset URL and notes (common for all tests)
    resource_url = "http://example.com"
    url_dataset_description = "This is a test URL dataset."
    
    # Step 2a: Test StreamProcessing
    stream_processing = StreamProcessing(refresh_rate="5 seconds", data_key="results")
    url_dataset_name_stream = generate_random_string()
    url_dataset_title_stream = f"Stream URL Dataset {url_dataset_name_stream}"

    # Register the Stream URL dataset
    response_create_stream = client.register_url(
        resource_name=url_dataset_name_stream,
        resource_title=url_dataset_title_stream,
        owner_org=owner_org,
        resource_url=resource_url,
        file_type="stream",
        processing=stream_processing,
        notes=url_dataset_description
    )
    
    # Check if the Stream URL dataset was created successfully
    assert "id" in response_create_stream
    assert response_create_stream.get("id") is not None
    
    # Step 2b: Test CSVProcessing
    csv_processing = CSVProcessing(delimiter=",", header_line=1, start_line=2)
    url_dataset_name_csv = generate_random_string()
    url_dataset_title_csv = f"CSV URL Dataset {url_dataset_name_csv}"

    # Register the CSV URL dataset
    response_create_csv = client.register_url(
        resource_name=url_dataset_name_csv,
        resource_title=url_dataset_title_csv,
        owner_org=owner_org,
        resource_url=resource_url,
        file_type="CSV",
        processing=csv_processing,
        notes=url_dataset_description
    )
    
    # Check if the CSV URL dataset was created successfully
    assert "id" in response_create_csv
    assert response_create_csv.get("id") is not None
    
    # Step 2c: Test JSONProcessing
    json_processing = JSONProcessing(info_key="count", data_key="results")
    url_dataset_name_json = generate_random_string()
    url_dataset_title_json = f"JSON URL Dataset {url_dataset_name_json}"

    # Register the JSON URL dataset
    response_create_json = client.register_url(
        resource_name=url_dataset_name_json,
        resource_title=url_dataset_title_json,
        owner_org=owner_org,
        resource_url=resource_url,
        file_type="JSON",
        processing=json_processing,
        notes=url_dataset_description
    )
    
    # Check if the JSON URL dataset was created successfully
    assert "id" in response_create_json
    assert response_create_json.get("id") is not None

    # Step 3: Delete all datasets (Stream, CSV, JSON)
    response_delete_stream = client.delete_resource(resource_name=url_dataset_name_stream)
    assert response_delete_stream.get("message") == f"{url_dataset_name_stream} deleted successfully"

    response_delete_csv = client.delete_resource(resource_name=url_dataset_name_csv)
    assert response_delete_csv.get("message") == f"{url_dataset_name_csv} deleted successfully"

    response_delete_json = client.delete_resource(resource_name=url_dataset_name_json)
    assert response_delete_json.get("message") == f"{url_dataset_name_json} deleted successfully"
    
    # Step 4: Delete the organization
    response_delete_org = client.delete_organization(organization_name=org_name)
    assert response_delete_org.get("message") == "Organization deleted successfully"
