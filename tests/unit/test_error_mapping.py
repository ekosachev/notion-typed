import pytest

from notion_typed.exceptions import APIError, AuthenticationError, PermissionError, RateLimitError


def test_authentication_error(client, mock_httpx_request):
    _ = mock_httpx_request(status_code=401, json_data={"message": "Unauthorized"})

    with pytest.raises(AuthenticationError):
        client._request("GET", "/v1/pages/123")


def test_permission_error(client, mock_httpx_request):
    _ = mock_httpx_request(
        status_code=403, json_data={"message": "API token does not have access to this resource."}
    )

    with pytest.raises(PermissionError):
        client._request("GET", "/v1/pages/123")


def test_rate_limit_error(client, mock_httpx_request):
    _ = mock_httpx_request(
        status_code=429,
        json_data={"message": "You have been rate limited. Please try again in a few minutes."},
    )

    with pytest.raises(RateLimitError):
        client._request("GET", "/v1/pages/123")


def test_api_error_error(client, mock_httpx_request):
    _ = mock_httpx_request(status_code=418, json_data={"message": "I am a teapot"})

    with pytest.raises(APIError):
        client._request("GET", "/v1/pages/123")
