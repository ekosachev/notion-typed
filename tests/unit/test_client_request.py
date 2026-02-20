def test_successful_request(client, mocker):
    fake_response = mocker.Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {"id": "123"}

    mocker.patch("httpx.request", return_value=fake_response)

    result = client._request("GET", "/v1/pages/123")

    assert result == {"id": "123"}


def test_client_url_builder(client, mocker):
    fake_response = mocker.Mock()

    fake_response.status_code = 200
    fake_response.json.return_value = {"id": "123"}

    mock_request = mocker.patch("httpx.request", return_value=fake_response)

    route = "/v1/pages/123"

    _ = client._request("GET", route)

    called_url = mock_request.call_args.kwargs["url"]
    assert called_url == client.base_url + "/v1/pages/123"


def test_client_param_handling(client, mocker):
    fake_response = mocker.Mock()

    fake_response.status_code = 200
    fake_response.json.return_value = {"id": "123"}

    params = {"param1": "value1"}

    mock_request = mocker.patch("httpx.request", return_value=fake_response)

    _ = client._request("GET", "/v1/pages/123", params=params)

    sent_params = mock_request.call_args.kwargs["params"]

    assert sent_params == params


def test_client_content_type(client, mocker):
    fake_response = mocker.Mock()

    fake_response.status_code = 200
    fake_response.json.return_value = {"id": "123"}

    mock_request = mocker.patch("httpx.request", return_value=fake_response)

    _ = client._request("GET", "/v1/pages/123")

    sent_headers = mock_request.call_args.kwargs["headers"]

    assert sent_headers["Content-Type"] == "application/json"
