import pytest

from notion_typed.models.page import Page


def test_successfull_get_page(client, mock_httpx_request, page):
    _ = mock_httpx_request(status_code=200, json_data=page)

    result = client.get_page("123")

    assert isinstance(result, Page)


def test_title_extraction(client, mock_httpx_request, page):
    _ = mock_httpx_request(status_code=200, json_data=page)

    result: Page = client.get_page("123")

    parsed_title = result.title

    assert parsed_title == "Bug bash"


def test_composite_title_extraction(client, mock_httpx_request, page):
    _ = mock_httpx_request(
        status_code=200,
        json_data=page
        | {
            "properties": {
                "Title": {
                    "type": "title",
                    "title": [{"plain_text": "Hello "}, {"plain_text": "world!"}],
                }
            }
        },
    )

    result: Page = client.get_page("123")
    parsed_title = result.title

    assert parsed_title == "Hello world!"


def test_custom_named_title_extraction(client, mock_httpx_request, page):
    _ = mock_httpx_request(
        status_code=200,
        json_data=page
        | {
            "properties": {
                "Title": {},
                "Custom title name": {
                    "type": "title",
                    "title": [{"plain_text": "A custom title prop"}],
                },
            }
        },
    )

    result: Page = client.get_page("123")
    parsed_title = result.title

    assert parsed_title == "A custom title prop"


def test_no_title_exception(client, mock_httpx_request, page):
    _ = mock_httpx_request(
        status_code=200,
        json_data=page
        | {
            "properties": {
                "Title": {},
            }
        },
    )

    with pytest.raises(ValueError):
        _ = client.get_page("123")
