import requests


def register_url(self, resource_name: str, resource_title: str, owner_org: str,
                 resource_url: str, api_token: str, notes: str = "") -> dict:
    """
    Create a new URL resource in the sciDX system.

    Parameters
    ----------
    resource_name : str
        The name of the resource.
    resource_title : str
        The title of the resource.
    owner_org : str
        The name of the organization.
    resource_url : str
        The URL of the resource.
    api_token : str
        The authentication token from the sciDX REST API.
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
    url = f"{self.api_url}/url"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    payload = {
        "resource_name": resource_name,
        "resource_title": resource_title,
        "owner_org": owner_org,
        "resource_url": resource_url,
        "notes": notes
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        return response.json()
    else:
        error_message = (
            f"Failed to create URL resource. "
            f"Request URL: {url}\n"
            f"Payload: {payload}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)
