from typing import Callable, Any, Awaitable

from telethon.events import NewMessage

ERROR_HANDLER_TYPE = Callable[[NewMessage.Event, Exception], Awaitable[Any]]
BOT_ERROR_HANDLER_TYPE = Callable[[Callable[[...], Awaitable[Any]], NewMessage.Event, Exception], Awaitable[Any]]
