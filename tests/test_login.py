import os
import pytest
from requests.exceptions import HTTPError
from . import conftest

SCIDX_USER=os.environ["SCIDX_USER"]
SCIDX_PASSWORD=os.environ["SCIDX_PASSWORD"]

# Test for successful login to the real API
def test_login_success_real_api(client):
    """
    Test that the login function correctly sets the access token
    when authenticating against the real API at localhost:8765.
    """
    client.login(username=SCIDX_USER, password=SCIDX_PASSWORD)
    
    # Check that the token was set and is not None or empty
    assert client.token is not None
    assert len(client.token) > 0

# Test for failed login to the real API
def test_login_failure_real_api(client):
    """
    Test that the login function raises an HTTPError when the 
    authentication request fails against the real API at 
    localhost:8765.
    """
    # Attempt to login with incorrect credentials
    with pytest.raises(HTTPError) as exc_info:
        client.login(username="wrong_user", password="wrong_password")
    
    # Check the exception message for the correct status code
    assert "Failed to authenticate user" in str(exc_info.value)
    assert "Response Status Code" in str(exc_info.value)
