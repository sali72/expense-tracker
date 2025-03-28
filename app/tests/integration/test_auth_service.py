import requests

from app.core.config import settings


def test_auth_token_acquisition():
    """Test that we can get a valid token from the auth service."""
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = "grant_type=password&username=user%40example.com&password=stringst"

    response = requests.post(
        settings.AUTH_SERVICE_TOKEN_URL, headers=headers, data=data
    )

    assert response.status_code == 200, f"Failed to get token: {response.text}"
    token_data = response.json()
    assert "access_token" in token_data
    assert "token_type" in token_data
    assert token_data["token_type"] == "bearer"
