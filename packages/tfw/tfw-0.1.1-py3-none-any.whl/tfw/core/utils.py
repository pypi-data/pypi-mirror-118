from functools import partial
from html import escape as _escape
import inspect
from typing import Any, Callable, Awaitable
from telethon import events

from tfw.internal.utils import annotation_to_str
from tfw.core import exceptions

escape_html = partial(_escape, quote=False)


def generate_command_usage(signature: inspect.Signature) -> str:
    res = '{COMMAND} '
    params = []
    for param in signature.parameters.values():
        if param.kind == inspect.Parameter.POSITIONAL_ONLY:
            continue
        annotation = annotation_to_str(param.annotation)
        if param.default == inspect.Parameter.empty:
            if param.kind == inspect.Parameter.VAR_POSITIONAL:
                params.append(f'[{annotation} {param.name}...]')
            else:
                params.append(f'<{annotation} {param.name}>')
        else:
            params.append(f'[{annotation} {param.name}={repr(param.default)}]')

    return res + ' '.join(params)


async def wrong_usage_handler(func: Callable[[...], Awaitable[Any]], event: events.NewMessage.Event,
                              exception: exceptions.WrongUsageError):
    usage = generate_command_usage(inspect.signature(func)).format(COMMAND=event.raw_text.split()[0])
    await event.reply(f'Error: {exception.kind.value.format(*exception.args)}\nUsage: {escape_html(usage)}')


