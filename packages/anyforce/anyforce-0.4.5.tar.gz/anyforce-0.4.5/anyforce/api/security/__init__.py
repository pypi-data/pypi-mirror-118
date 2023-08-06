from typing import Any, Callable, Coroutine, Union

from fastapi import Depends
from passlib.context import CryptContext

from ..g import set

password_context: CryptContext = CryptContext(schemes=["bcrypt"])


async def with_context(
    get_current_user: Callable[..., Union[Coroutine[Any, Any, Any], Any]]
):
    def f(current_user: Any = Depends(get_current_user)):
        set("user", current_user)
        return current_user

    return f
