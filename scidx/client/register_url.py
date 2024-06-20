import requests

def register_url(self, resource_name: str, resource_title: str, owner_org: str,
                 resource_url: str, notes: str = "") -> dict:
    """
    Add a URL resource to the sciDX system.

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
    url = f"{self.api_url}/resource"
    payload = {
        "resource_name": resource_name,
        "resource_title": resource_title,
        "owner_org": owner_org,
        "resource_url": resource_url,
        "notes": notes
    }
    response = requests.post(url, json=payload)
    print(f"Request URL: {url}")
    print(f"Payload: {payload}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")
    if response.status_code == 201:
        resource_id = response.json().get('id')
        if resource_id:
            try:
                resource_payload = {
                    "package_id": resource_id,
                    "url": resource_url,
                    "name": resource_name,
                    "description": f"Resource pointing to {resource_url}",
                    "format": "html"
                }
                resource_response = requests.post(f"{self.api_url}/resource", json=resource_payload)
                print(f"Resource Request URL: {self.api_url}/resource")
                print(f"Resource Payload: {resource_payload}")
                print(f"Resource Response Status Code: {resource_response.status_code}")
                print(f"Resource Response Content: {resource_response.content.decode('utf-8')}")
                if resource_response.status_code == 201:
                    return response.json()
                else:
                    error_message = (
                        f"Failed to create resource for the URL. "
                        f"Resource Request URL: {self.api_url}/resource\n"
                        f"Resource Payload: {resource_payload}\n"
                        f"Resource Response Status Code: {resource_response.status_code}\n"
                        f"Resource Response Content: {resource_response.content.decode('utf-8')}"
                    )
                    raise requests.exceptions.HTTPError(error_message, response=resource_response)
            except requests.exceptions.RequestException as e:
                error_message = f"Failed to create resource: {str(e)}"
                raise requests.exceptions.HTTPError(error_message)
        else:
            raise requests.exceptions.HTTPError("Failed to retrieve the resource ID from the response.")
    else:
        error_message = (
            f"Failed to create URL resource. "
            f"Request URL: {url}\n"
            f"Payload: {payload}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)
