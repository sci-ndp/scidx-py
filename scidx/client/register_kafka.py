import requests

def register_kafka(self, dataset_name: str, dataset_title: str, owner_org: str,
                   kafka_topic: str, kafka_host: str, kafka_port: int, 
                   dataset_description: str = "") -> dict:
    """
    Create a new Kafka dataset in the sciDX system.

    Parameters
    ----------
    dataset_name : str
        The name of the dataset.
    dataset_title : str
        The title of the dataset.
    owner_org : str
        The name of the organization.
    kafka_topic : str
        The Kafka topic name.
    kafka_host : str
        The Kafka host address.
    kafka_port : int
        The Kafka port number.
    dataset_description : str, optional
        The description of the dataset (default is an empty string).

    Returns
    -------
    dict
        A dictionary containing the response from the API.

    Raises
    ------
    HTTPError
        If the API request fails with detailed error information.
    """
    url = f"{self.api_url}/kafka"
    payload = {
        "dataset_name": dataset_name,
        "dataset_title": dataset_title,
        "owner_org": owner_org,
        "kafka_topic": kafka_topic,
        "kafka_host": kafka_host,
        "kafka_port": kafka_port,
        "dataset_description": dataset_description
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        error_message = (
            f"Failed to create Kafka dataset. "
            f"Request URL: {url}\n"
            f"Payload: {payload}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)