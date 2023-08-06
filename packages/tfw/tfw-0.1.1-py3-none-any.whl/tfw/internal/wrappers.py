import inspect
import warnings
from functools import wraps
from traceback import print_exc
from typing import TYPE_CHECKING, Optional, List, Any, Type, Union, Callable, Dict, Awaitable

from telethon.events import NewMessage, CallbackQuery, StopPropagation
from telethon.events.common import EventCommon

from tfw.core import convert_arguments
from tfw.core.converters import user_converter, sender_converter, TEXT_DEFAULT_CONVERTERS, \
    CTX_DEFAULT_CONVERTERS, CONVERTERS_TYPE
from tfw.internal.utils import fullmatch_pattern, is_correct_command, INVALID_COMMAND_MESSAGE, \
    build_regexp, validate_error_for_handler
from tfw.types import ERROR_HANDLER_TYPE

if TYPE_CHECKING:
    from tfw import Bot


def _event_wrapper(event_type: Type[Union[CallbackQuery, NewMessage]]):
    def _event_wrapper_inner(self: 'Bot', pattern: Optional[str] = None, state: Optional[str] = None, *args,
                             fullmatch=True, stop_propagation=True, **kwargs):
        ctx_converters = CTX_DEFAULT_CONVERTERS.copy()
        if self.user_model is not None:
            async def convert_tg_sender(evt: EventCommon):
                return await self.user_model.from_tg(await sender_converter(evt))

            ctx_converters[self.user_model] = convert_tg_sender

        if fullmatch:
            pattern = fullmatch_pattern(pattern)

        if state is not None and self.user_model is None:
            raise ValueError("cannot use FSM without defined User model")

        if event_type == NewMessage and 'outgoing' not in kwargs and 'incoming' not in kwargs:
            kwargs['incoming'] = True
            # we should not receive outgoing messages from other sessions unless stated otherwise

        # TODO state check

        def decorator(func):
            @wraps(func)
            async def inner(event: event_type.Event):
                try:
                    resolved = await convert_arguments(event, inspect.signature(func),
                                                       ctx_converters=ctx_converters,
                                                       parse_text=False)
                    return await func(*resolved)
                except Exception:
                    print_exc()  # TODO: logging or sth else
                if stop_propagation:  # TODO: lookup default action in Bot, not hardcode it
                    raise StopPropagation

            self._after_sign_in_callbacks.append(
                lambda: self.add_event_handler(inner, event_type(*args, pattern=pattern, **kwargs))
            )

            return func

        return decorator

    return _event_wrapper_inner


# noinspection PyProtectedMember
class Command:
    bot: 'Bot'
    func: Callable[[...], Awaitable[Any]]
    stop_propagation: bool
    _default_error_handler: Optional[ERROR_HANDLER_TYPE]
    _error_handlers: Dict[Type[Exception], ERROR_HANDLER_TYPE]
    _ctx_converters: CONVERTERS_TYPE
    _text_converters: CONVERTERS_TYPE

    def __init__(self, bot: 'Bot', func: Callable[[...], Awaitable[Any]], *, stop_propagation=True):
        self.bot = bot
        self.func = func
        self.stop_propagation = stop_propagation
        self._default_error_handler = None
        self._error_handlers = {}

        self._ctx_converters = CTX_DEFAULT_CONVERTERS.copy()
        self._text_converters = TEXT_DEFAULT_CONVERTERS.copy()
        if bot.user_model is not None:
            async def convert_tg_sender(evt: EventCommon):
                return await bot.user_model.from_tg(await sender_converter(evt))

            self._ctx_converters[bot.user_model] = convert_tg_sender

            async def convert_tg_user(evt: EventCommon, val: str):
                return await bot.user_model.from_tg(await user_converter(evt, val))

            self._text_converters[bot.user_model] = convert_tg_user

    def error_handler(self, excs=None):
        if not excs:
            excs = []

        def decorator(func: ERROR_HANDLER_TYPE):
            for exc in excs:
                validate_error_for_handler(exc)
                if exc in self._error_handlers:
                    warnings.warn(f'Command {self.func.__qualname__} already has error_handler for '
                                  f'{exc.__qualname__}, overriding')
                self._error_handlers[exc] = func
            if not excs:
                if self._default_error_handler is not None:
                    warnings.warn(f'Command {self.func.__qualname__} already has default error_handler, overriding')
                self._default_error_handler = func
            return func

        return decorator

    async def _handle_event(self, event: NewMessage.Event):
        try:
            resolved = await convert_arguments(event, inspect.signature(self.func),
                                               ctx_converters=self._ctx_converters,
                                               text_converters=self._text_converters,
                                               parse_text=True)
            return await self.func(*resolved)
        except StopPropagation:
            raise
        except Exception as err:
            await self._dispatch_error(event, err)
        if self.stop_propagation:
            raise StopPropagation

    async def _dispatch_error(self, event: NewMessage.Event, err: Exception):
        if type(err) in self._error_handlers:
            await self._error_handlers[type(err)](event, err)
        elif type(err) in self.bot._error_handlers:
            await self.bot._error_handlers[type(err)](self.func, event, err)
        elif self._default_error_handler:
            await self._default_error_handler(event, err)
        elif self.bot._default_error_handler:
            await self.bot._default_error_handler(self.func, event, err)
        else:
            raise err  # could not handle


# noinspection PyProtectedMember
class CommandFactory:
    bot: 'Bot'

    def __init__(self, bot: 'Bot'):
        self.bot = bot

    # Signature here for the sake of autocomplete
    def __call__(self, aliases: Optional[Union[str, List[str]]] = None, state: Optional[str] = None,
                 name: Optional[str] = None, stop_propagation: bool = True):
        if aliases is None:
            aliases = []
        elif isinstance(aliases, str):
            aliases = []
            name = aliases

        if not all(is_correct_command(i) for i in aliases):
            raise ValueError(INVALID_COMMAND_MESSAGE)

        def decorator(func: Callable[[...], Awaitable[Any]]):
            obj = Command(self.bot, func, stop_propagation=stop_propagation)
            all_commands = aliases + [name or func.__name__]
            if not is_correct_command(name or func.__name__):
                raise ValueError(INVALID_COMMAND_MESSAGE)

            def on_signed_in():
                regexp = build_regexp(all_commands, self.bot.me.username)
                self.bot.add_event_handler(obj._handle_event, NewMessage(pattern=regexp))

            self.bot._after_sign_in_callbacks.append(on_signed_in)
            return obj

        return decorator
