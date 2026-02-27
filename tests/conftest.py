from typing import Any

import pytest

from src.notion_typed.client import Client


@pytest.fixture
def client():
    return Client(token="test_token")


@pytest.fixture
def mock_httpx_request(mocker):
    def _mock(*, status_code: int = 200, json_data: dict[str, Any] | None = None):
        fake_response = mocker.Mock()
        fake_response.status_code = status_code
        fake_response.json.return_value = json_data or {}

        mock_request = mocker.patch("httpx.request", return_value=fake_response)

        return mock_request, fake_response

    return _mock
