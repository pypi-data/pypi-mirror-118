from typing import Union, Callable, Dict

from telethon import events
from telethon.events.common import EventCommon
from telethon.tl import custom
from telethon.tl.custom.sendergetter import SenderGetter
from telethon.tl.types import User as TgUser, InputUser, InputPeerUser

from . import exceptions


def _bool_converter(val: str) -> bool:
    val = val.lower()
    if val in ['n', 'no', '0', 'false', 'f', '-']:
        return False
    if val in ['y', 'yes', '1', 'true', 't', '+']:
        return True
    raise ValueError(f'unknown boolean value: {repr(val)}')


async def input_user_converter(evt: EventCommon, val: Union[str, int]) -> InputPeerUser:
    if isinstance(val, str):
        try:
            return await input_user_converter(evt, int(val))
        except ValueError:
            pass
    res = await evt.client.get_input_entity(val)
    if not isinstance(res, InputPeerUser):
        raise ValueError(f'Argument {val} got converted to {type(res)}, not User')
    return res


async def user_converter(evt: EventCommon, val: str) -> TgUser:
    return await evt.client.get_entity(await input_user_converter(evt, val))


TEXT_DEFAULT_CONVERTERS = {
    int: int,
    str: str,
    float: float,
    bool: _bool_converter,
    InputPeerUser: input_user_converter,
    InputUser: input_user_converter,
    TgUser: user_converter,
}


async def message_converter(evt: EventCommon):
    if isinstance(evt, events.NewMessage.Event):
        return evt.message
    elif isinstance(evt, events.CallbackQuery.Event):
        return await evt.get_message()
    else:
        # TODO: чекнуть остальные ивенты
        raise exceptions.BadSignatureError(f'Event {type(evt)} has no message')


async def input_sender_converter(evt: EventCommon):
    if isinstance(evt, SenderGetter) or isinstance(evt, events.NewMessage.Event):
        return await evt.get_input_sender()
    else:
        raise exceptions.BadSignatureError(f'Unable to get sender for event {type(evt)}')


async def sender_converter(evt: EventCommon):
    return await evt.client.get_entity(await input_sender_converter(evt))


CTX_DEFAULT_CONVERTERS = {
    EventCommon: lambda x: x,
    custom.Message: message_converter,
    # TODO: does it work correctly with GroupAnonymousBot or discussion posts?
    InputPeerUser: input_sender_converter,
    InputUser: input_sender_converter,
    TgUser: sender_converter,
}

CONVERTERS_TYPE = Dict[type, Callable]
