import pytest

from src.notion_typed.client import Client


@pytest.fixture
def client():
    return Client(token="test_token")
