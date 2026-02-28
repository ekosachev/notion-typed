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


@pytest.fixture
def page():
    return {
        "object": "page",
        "id": "be633bf1-dfa0-436d-b259-571129a590e5",
        "created_time": "2022-10-24T22:54:00.000Z",
        "last_edited_time": "2023-03-08T18:25:00.000Z",
        "created_by": {"object": "user", "id": "c2f20311-9e54-4d11-8c79-7398424ae41e"},
        "last_edited_by": {"object": "user", "id": "9188c6a5-7381-452f-b3dc-d4865aa89bdf"},
        "cover": None,
        "icon": {"type": "emoji", "emoji": "🐞"},
        "parent": {"type": "database_id", "database_id": "a1d8501e-1ac1-43e9-a6bd-ea9fe6c8822b"},
        "archived": False,
        "in_trash": False,
        "properties": {
            "Due date": {
                "id": "M%3BBw",
                "type": "date",
                "date": {"start": "2023-02-23", "end": None, "time_zone": None},
            },
            "Status": {
                "id": "Z%3ClH",
                "type": "status",
                "status": {
                    "id": "86ddb6ec-0627-47f8-800d-b65afd28be13",
                    "name": "Not started",
                    "color": "default",
                },
            },
            "Title": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {"content": "Bug bash", "link": None},
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "strikethrough": False,
                            "underline": False,
                            "code": False,
                            "color": "default",
                        },
                        "plain_text": "Bug bash",
                        "href": None,
                    }
                ],
            },
        },
        "url": "https://www.notion.so/Bug-bash-be633bf1dfa0436db259571129a590e5",
        "public_url": "https://jm-testing.notion.site/p1-6df2c07bfc6b4c46815ad205d132e22d",
    }
