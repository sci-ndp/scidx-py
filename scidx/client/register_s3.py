import requests

def register_s3(self, resource_name: str, resource_title: str, owner_org: str,
                resource_s3: str, notes: str = "") -> dict:
    """
    Create a new S3 resource in the sciDX system.

    Parameters
    ----------
    resource_name : str
        The name of the resource.
    resource_title : str
        The title of the resource.
    owner_org : str
        The name of the organization.
    resource_s3 : str
        The S3 path of the resource.
    notes : str, optional
        Additional notes about the resource (default is an empty string).

    Returns
    -------
    dict
        A dictionary containing the response from the API.

    Raises
    ------
    HTTPError
        If the API request fails with detailed error information.
    """
    url = f"{self.api_url}/s3"
    payload = {
        "resource_name": resource_name,
        "resource_title": resource_title,
        "owner_org": owner_org,
        "resource_s3": resource_s3,
        "notes": notes
    }
    response = requests.post(url, json=payload)
    print(f"Request URL: {url}")
    print(f"Payload: {payload}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")
    if response.status_code == 201:
        return response.json()
    else:
        error_message = (
            f"Failed to create S3 resource. "
            f"Request URL: {url}\n"
            f"Payload: {payload}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)
