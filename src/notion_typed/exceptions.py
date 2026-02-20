class NotionClientError(Exception):
    """Base exception for all Notion client errors."""


class APIError(NotionClientError):
    def __init__(self, status_code: int, message: str, response: dict | None = None):
        self.status_code = status_code
        self.response = response
        super().__init__(f"{status_code}: {message}")


class AuthenticationError(APIError):
    pass


class PermissionError(APIError):
    pass


class RateLimitError(APIError):
    pass
