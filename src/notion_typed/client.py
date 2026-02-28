import logging
from typing import Any, Literal

import httpx

from notion_typed.enums import NotionVersion
from notion_typed.exceptions import APIError, AuthenticationError, PermissionError, RateLimitError
from notion_typed.models.page import Page

DEFAULT_VERSION = NotionVersion.V2025_09_03
DEFAULT_BASE_URL = "https://api.notion.com"

logger = logging.getLogger(__name__)


class Client:
    token: str
    notion_version: NotionVersion = DEFAULT_VERSION
    base_url: str = DEFAULT_BASE_URL

    def __init__(self, token: str) -> None:
        self.token = token

    def _request(
        self,
        method: Literal["GET", "POST", "PATCH", "DELETE"],
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:

        if headers is None:
            headers = {}

        headers["Authorization"] = f"Bearer {self.token}"
        headers["Notion-Version"] = f"{self.notion_version}"
        headers["Content-Type"] = "application/json"

        full_url = self.base_url + path

        logger.debug("Sending request: %s, %s", method, full_url)
        response = httpx.request(
            method=method,
            url=full_url,
            json=json,
            params=params,
            headers=headers,
        )

        logger.debug("Received response: %s %s %s", response.status_code, method, full_url)

        try:
            data = response.json()
        except ValueError:
            data = {}

        exc: APIError | None = None

        if response.status_code == 401:
            exc = AuthenticationError(401, data.get("message", ""), data)
        elif response.status_code == 403:
            exc = PermissionError(403, data.get("message", ""), data)
        elif response.status_code == 429:
            exc = RateLimitError(429, data.get("message", ""), data)
        elif response.status_code >= 400:
            exc = APIError(response.status_code, data.get("message", ""), data)

        if exc is not None:
            logger.warning(
                "Request failed with status %s for %s %s: %s",
                response.status_code,
                method,
                full_url,
                getattr(exc, "response", None),
            )
            raise exc

        return data

    def get_page(self, id: str) -> Page:
        base_url = "/v1/pages/"

        response = self._request("GET", base_url + id)
        return Page.from_api(response)
