from typing import Any

from pydantic import BaseModel, PrivateAttr


def extract_title(data: dict[str, Any]) -> str:
    properties = data.get("properties", {})
    for prop in properties.values():
        if prop.get("type") == "title":
            title_items: list = prop.get("title", [])

            full_title = "".join(item.get("plain_text", "") for item in title_items)

            return full_title
    raise ValueError("No title property found")


class Page(BaseModel):
    id: str
    title: str

    _raw: dict[str, Any] = PrivateAttr()

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Page":
        title = extract_title(data)

        page = cls(
            id=data["id"],
            title=title,
        )

        page._raw = data

        return page
