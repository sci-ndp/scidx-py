import requests

def create_datasource(self, dataset_name: str, dataset_title: str, organization_id: str,
                      resource_url: str, resource_name: str, dataset_description: str,
                      resource_description: str, resource_format: str) -> str:
    """
    Create a new data source in the sciDX system.

    Parameters
    ----------
    dataset_name : str
        The name of the dataset.
    dataset_title : str
        The title of the dataset.
    organization_id : str
        The ID of the organization.
    resource_url : str
        The URL of the resource.
    resource_name : str
        The name of the resource.
    dataset_description : str
        The description of the dataset.
    resource_description : str
        The description of the resource.
    resource_format : str
        The format of the resource.

    Returns
    -------
    str
        The ID of the created dataset.

    Raises
    ------
    Exception
        If there is an error creating the dataset.
    """
    url = f"{self.api_url}/"
    payload = {
        "dataset_name": dataset_name,
        "dataset_title": dataset_title,
        "organization_id": organization_id,
        "resource_url": resource_url,
        "resource_name": resource_name,
        "dataset_description": dataset_description,
        "resource_description": resource_description,
        "resource_format": resource_format
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()
