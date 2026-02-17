# Notion Typed
## Philosophy

> Don't waste time communicating with Notion, write what matters for the project

This project aims to provide:
- A fully typed Notion API client
- Async and sync support
- Schema-aware ORM layer
- Explicit and predictable behavior

## Why this library exists?

Interfacing with Notion API can be difficult, and setting up proper typing can inflate your codebase with stuff that does not relate to the project itself. **Notion Typed** is a way to delegate all the difficult stuff and focus on doing what you set out to do

## Some examples (subject to change, DX not final)

```py
"""Retrieve a page using id"""
from notion_typed import Client

client = Client(token="...")

page = client.pages.retrieve(page_id)
```

```py
"""Sync client querying"""
from notion_typed import *

class Task(BaseDatabaseEntry):
    __data_source_id__ = "..."

    title = Title
    status = Status
    deadline = NotionDatetime

client = Client(token="...")

tasks = Task.query(client)
    .where(Task.status.not_in_group(StatusGroup.Done))
    .order_by(Task.deadline.asc())
    .limit(10)
    .all()
```
```py
"""Async client querying"""
from notion_typed import *

class Task(BaseDatabaseEntry):
    __data_source_id__ = "..."

    title = Title
    status = Status
    deadline = NotionDatetime

async_client = AsyncClient(token="...")

tasks = await Task.query(async_client)
    .where(Task.status.not_in_group(StatusGroup.Done))
    .order_by(Task.deadline.asc())
    .all()
```