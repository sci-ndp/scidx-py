import requests

def construct_s3_url(bucket_name: str) -> str:
    base_url = "https://{}.s3.amazonaws.com/index.html"
    return base_url.format(bucket_name)

def register_s3bucket(self, bucket_name: str, bucket_title: str, owner_org: str, notes: str = "") -> dict:
    """
    Add a pointer to an S3 bucket in the sciDX system.

    Parameters
    ----------
    bucket_name : str
        The name of the S3 bucket.
    bucket_title : str
        The title of the S3 bucket.
    owner_org : str
        The name of the organization.
    notes : str, optional
        Additional notes about the bucket (default is an empty string).

    Returns
    -------
    dict
        A dictionary containing the response from the API.

    Raises
    ------
    HTTPError
        If the API request fails with detailed error information.
    """
    url = f"{self.api_url}/s3bucket"
    payload = {
        "bucket_name": bucket_name,
        "bucket_title": bucket_title,
        "owner_org": owner_org,
        "notes": notes
    }
    response = requests.post(url, json=payload)
    print(f"Request URL: {url}")
    print(f"Payload: {payload}")
    print(f"Response Status Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")
    if response.status_code == 201:
        bucket_id = response.json().get('id')
        if bucket_id:
            try:
                resource_url = construct_s3_url(bucket_name)
                resource_payload = {
                    "package_id": bucket_id,
                    "url": resource_url,
                    "name": bucket_name,
                    "description": f"Pointer to S3 bucket {bucket_name}",
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
                        f"Failed to create resource for the S3 bucket. "
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
            raise requests.exceptions.HTTPError("Failed to retrieve the bucket ID from the response.")
    else:
        error_message = (
            f"Failed to create S3 bucket. "
            f"Request URL: {url}\n"
            f"Payload: {payload}\n"
            f"Response Status Code: {response.status_code}\n"
            f"Response Content: {response.content.decode('utf-8')}"
        )
        raise requests.exceptions.HTTPError(error_message, response=response)
