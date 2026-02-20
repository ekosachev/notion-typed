from src.notion_typed.client import Client


def test_request_auth_header(mocker):
    fake_response = mocker.Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"id": "page_123"}

    mock_request = mocker.patch("httpx.request", return_value=fake_response)

    client = Client(token="secret")
    res = client._request("GET", "/v1/pages/page_123")

    mock_request.assert_called_once()
    headers = mock_request.call_args.kwargs["headers"]
    assert headers["Authorization"] == "Bearer secret"
    assert headers["Notion-Version"] == str(client.notion_version)
    assert res == {"id": "page_123"}
