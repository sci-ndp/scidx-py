import pytest
import string
import random
import time  # Import the time module to add a delay
from scidx.client import sciDXClient
from scidx.client import CSVProcessing

# Helper function to generate a random string
def generate_random_string(length=8):
    """
    Generate a random string of fixed length.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

# Test for updating an existing Kafka dataset
def test_update_kafka_dataset():
    """
    Test the ability to update an existing Kafka dataset in the system.
    """
    # Create a client instance with the actual API URL
    client = sciDXClient(api_url="http://localhost:8765")
    
    # Set the token for authentication
    client.token = "test"
    
    # Step 1: Create a random organization to associate with the resource
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

    # Step 2: Create a random Kafka dataset
    kafka_dataset_name = generate_random_string()
    kafka_dataset_title = f"Kafka Dataset {kafka_dataset_name}"
    kafka_topic = generate_random_string(6)
    kafka_host = "localhost"
    kafka_port = 9092
    kafka_dataset_description = "This is a test Kafka dataset."

    # Register the Kafka dataset
    response_create_kafka = client.register_kafka(
        dataset_name=kafka_dataset_name,
        dataset_title=kafka_dataset_title,
        owner_org=org_name,
        kafka_topic=kafka_topic,
        kafka_host=kafka_host,
        kafka_port=kafka_port,
        dataset_description=kafka_dataset_description
    )

    # Check if the Kafka dataset was created successfully
    assert "id" in response_create_kafka
    dataset_id = response_create_kafka.get("id")  # Extract the dataset ID for updating

    # Step 3: Update the Kafka dataset with new values
    updated_kafka_topic = generate_random_string(6)
    updated_kafka_host = "127.0.0.1"
    updated_dataset_title = f"Updated Kafka Dataset {kafka_dataset_name}"

    response_update_kafka = client.update_kafka(
        resource_id=dataset_id,
        dataset_name=kafka_dataset_name,
        dataset_title=updated_dataset_title,
        kafka_topic=updated_kafka_topic,
        kafka_host=updated_kafka_host
    )

    # Debugging: Print the update response to inspect it
    print("Update Kafka Dataset Response:", response_update_kafka)

    # Step 4: Verify that the update was successful
    assert response_update_kafka.get("message") == "Kafka dataset updated successfully"
    
    # (Optional) Step 5: Add a delay before querying the dataset again
    time.sleep(2)  # Wait for 2 seconds to allow the update to propagate

    # Query the dataset again to verify the updated values
    response_get_kafka = client.search_resource(dataset_name=kafka_dataset_name)
    
    # Debugging: Print the search response to inspect it
    print("Search Resource Response:", response_get_kafka)

    # Check if the updated title is reflected in the response under 'title'
    found = any(res['title'] == updated_dataset_title for res in response_get_kafka)
    assert found, f"Updated Kafka dataset not found with title {updated_dataset_title}"

    # Step 6: Delete the dataset and organization
    response_delete_kafka = client.delete_resource(resource_name=kafka_dataset_name)
    assert response_delete_kafka.get("message") == f"{kafka_dataset_name} deleted successfully"

    response_delete_org = client.delete_organization(organization_name=org_name)
    assert response_delete_org.get("message") == "Organization deleted successfully"
