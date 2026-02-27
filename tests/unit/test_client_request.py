def test_successful_request(client, mock_httpx_request):
    _ = mock_httpx_request(
        status_code=200,
        json_data={"id": "123"},
    )

    result = client._request("GET", "/v1/pages/123")

    assert result == {"id": "123"}


def test_client_url_builder(client, mock_httpx_request):
    mock_request, _ = mock_httpx_request(status_code=200, json_data={"id": "123"})

    route = "/v1/pages/123"

    _ = client._request("GET", route)

    called_url = mock_request.call_args.kwargs["url"]
    assert called_url == client.base_url + "/v1/pages/123"


def test_client_param_handling(client, mock_httpx_request):
    mock_request, _ = mock_httpx_request(status_code=200, json_data={"id": "123"})

    params = {"param1": "value1"}

    _ = client._request("GET", "/v1/pages/123", params=params)

    sent_params = mock_request.call_args.kwargs["params"]

    assert sent_params == params


def test_client_content_type(client, mock_httpx_request):
    mock_request, _ = mock_httpx_request(status_code=200, json_data={"id": "123"})

    _ = client._request("GET", "/v1/pages/123")

    sent_headers = mock_request.call_args.kwargs["headers"]

    assert sent_headers["Content-Type"] == "application/json"
