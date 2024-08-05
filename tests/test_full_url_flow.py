import pytest
import random
import string
from scidx.client import sciDXClient, StreamProcessing, CSVProcessing, TXTProcessing, JSONProcessing, NetCDFProcessing

# Constants
API_URL = "http://localhost:8000"
OWNER_ORG = "test_org"
USERNAME = "placeholder@placeholder.com"
PASSWORD = "placeholder"

def generate_unique_name():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

@pytest.fixture
def client():
    """
    Fixture to create and login the client for testing.
    """
    client = sciDXClient(API_URL)
    client.login(USERNAME, PASSWORD)
    return client

def verify_resource_exists(client, search_term, expected_name):
    """
    Verify that the resource exists in the search results.
    """
    search_results = client.search_resource(search_term=search_term)
    assert len(search_results) > 0, f"No resources found for search term: {search_term}"
    found = any(result["name"] == expected_name for result in search_results)
    assert found, f"Resource with name '{expected_name}' not found in search results."

def test_register_stream_url(client):
    """
    Test registering a Stream URL resource and verifying it via search.
    """
    resource_name = "stream_resource" + generate_unique_name()
    stream_processing = StreamProcessing(refresh_rate="5 seconds", data_key="results")
    
    print(f"\nExample StreamProcessing Payload: {stream_processing.to_dict()}")
    
    response = client.register_url(
        resource_name=resource_name,
        resource_title="Stream Resource Example",
        owner_org=OWNER_ORG,
        resource_url="http://example.com/stream",
        file_type="stream",
        processing=stream_processing,
        notes="This is a stream resource for testing.",
        extras={"key1": "value1", "key2": "value2"}
    )
    
    print(f"Registered Stream Resource Response: {response}")
    assert "id" in response
    assert response["id"] is not None

    # Verify the resource exists
    verify_resource_exists(client, search_term=resource_name, expected_name=resource_name)

def test_register_csv_url(client):
    """
    Test registering a CSV URL resource and verifying it via search.
    """
    resource_name = "csv_resource" + generate_unique_name()
    csv_processing = CSVProcessing(delimiter=",", header_line=1, start_line=2)
    
    print(f"\nExample CSVProcessing Payload: {csv_processing.to_dict()}")
    
    response = client.register_url(
        resource_name=resource_name,
        resource_title="CSV Resource Example",
        owner_org=OWNER_ORG,
        resource_url="http://example.com/csv",
        file_type="CSV",
        processing=csv_processing,
        notes="This is a CSV resource for testing.",
        extras={"key1": "value1", "key2": "value2"}
    )
    
    print(f"Registered CSV Resource Response: {response}")
    assert "id" in response
    assert response["id"] is not None

    # Verify the resource exists
    verify_resource_exists(client, search_term=resource_name, expected_name=resource_name)

def test_register_txt_url(client):
    """
    Test registering a TXT URL resource and verifying it via search.
    """
    resource_name = "txt_resource" + generate_unique_name()
    txt_processing = TXTProcessing(delimiter="\t", header_line=1, start_line=2)
    
    print(f"\nExample TXTProcessing Payload: {txt_processing.to_dict()}")
    
    response = client.register_url(
        resource_name=resource_name,
        resource_title="TXT Resource Example",
        owner_org=OWNER_ORG,
        resource_url="http://example.com/txt",
        file_type="TXT",
        processing=txt_processing,
        notes="This is a TXT resource for testing.",
        extras={"key1": "value1", "key2": "value2"}
    )
    
    print(f"Registered TXT Resource Response: {response}")
    assert "id" in response
    assert response["id"] is not None

    # Verify the resource exists
    verify_resource_exists(client, search_term=resource_name, expected_name=resource_name)

def test_register_json_url(client):
    """
    Test registering a JSON URL resource and verifying it via search.
    """
    resource_name = "json_resource" + generate_unique_name()
    json_processing = JSONProcessing(info_key="count", data_key="results")
    
    print(f"\nExample JSONProcessing Payload: {json_processing.to_dict()}")
    
    response = client.register_url(
        resource_name=resource_name,
        resource_title="JSON Resource Example",
        owner_org=OWNER_ORG,
        resource_url="http://example.com/json",
        file_type="JSON",
        processing=json_processing,
        notes="This is a JSON resource for testing.",
        extras={"key1": "value1", "key2": "value2"}
    )
    
    print(f"Registered JSON Resource Response: {response}")
    assert "id" in response
    assert response["id"] is not None

    # Verify the resource exists
    verify_resource_exists(client, search_term=resource_name, expected_name=resource_name)

def test_register_netcdf_url(client):
    """
    Test registering a NetCDF URL resource and verifying it via search.
    """
    resource_name = "netcdf_resource" + generate_unique_name()
    netcdf_processing = NetCDFProcessing(group="example_group")
    
    print(f"\nExample NetCDFProcessing Payload: {netcdf_processing.to_dict()}")
    
    response = client.register_url(
        resource_name=resource_name,
        resource_title="NetCDF Resource Example",
        owner_org=OWNER_ORG,
        resource_url="http://example.com/netcdf",
        file_type="NetCDF",
        processing=netcdf_processing,
        notes="This is a NetCDF resource for testing.",
        extras={"key1": "value1", "key2": "value2"}
    )
    
    print(f"Registered NetCDF Resource Response: {response}")
    assert "id" in response
    assert response["id"] is not None

    # Verify the resource exists
    verify_resource_exists(client, search_term=resource_name, expected_name=resource_name)

if __name__ == "__main__":
    pytest.main([__file__])
