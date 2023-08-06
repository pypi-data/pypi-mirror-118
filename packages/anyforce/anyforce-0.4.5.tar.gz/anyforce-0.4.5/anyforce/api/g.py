from typing import Any

from starlette_context import context


def get(k: str) -> Any:
    return context.data.get(k)  # type: ignore


def set(k: str, v: Any):
    context.data[k] = v  # type: ignore
