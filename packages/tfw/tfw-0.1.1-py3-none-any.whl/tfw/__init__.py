import logging
import warnings
from types import FunctionType
from typing import Dict, Union, TypeVar, Type, Optional, TYPE_CHECKING, List, Callable

from telethon import TelegramClient, events
from telethon.tl.types import User as TgUser

from tfw.internal.utils import validate_error_for_handler
from tfw.internal.wrappers import _event_wrapper, CommandFactory
from tfw.types import BOT_ERROR_HANDLER_TYPE
from tfw.core import exceptions, utils
from tfw.core.utils import wrong_usage_handler

try:
    import aiorun
except ImportError:
    aiorun = None

if TYPE_CHECKING:
    from tfw.models import User, StateComponent

USER_MODEL = TypeVar('USER_MODEL', bound='User')

DEFAULT_ERROR_HANDLERS = {exceptions.WrongUsageError: wrong_usage_handler}


class Bot(TelegramClient):
    user_model: Type[USER_MODEL]
    me: TgUser

    state_handlers: Dict[str, FunctionType]

    command: CommandFactory

    _error_handlers: Dict[Type[Exception], BOT_ERROR_HANDLER_TYPE]
    _default_error_handler: Optional[BOT_ERROR_HANDLER_TYPE]
    _after_sign_in_callbacks: List[Callable]

    def __init__(self, session: str, api_id: int, api_hash: str, bot_token: str,
                 user_model: Optional[Type[USER_MODEL]] = None, **kwargs):
        super().__init__(session, api_id=api_id, api_hash=api_hash, **kwargs)
        self.bot_token = bot_token
        self.parse_mode = kwargs.pop('parse_mode', 'html')
        self.state_handlers = {}
        self.user_model = user_model
        self.command = CommandFactory(self)
        self._error_handlers = DEFAULT_ERROR_HANDLERS.copy()
        self._default_error_handler = None
        self._after_sign_in_callbacks = []

    # @command

    def error_handler(self, excs=None):
        if not excs:
            excs = []

        def decorator(func: BOT_ERROR_HANDLER_TYPE):
            for exc in excs:
                validate_error_for_handler(exc)
                if exc in self._error_handlers:
                    warnings.warn(f'Bot instance already has error_handler for '
                                  f'{exc.__qualname__}, overriding')
                self._error_handlers[exc] = func
            if not excs:
                if self._default_error_handler is not None:
                    warnings.warn(f'Bot instance already has default error_handler, overriding')
                self._default_error_handler = func
            return func

        return decorator

    # fsm handlers

    def state_handler(self, *args):
        def decorator(func):
            state = _state or func.__name__
            self.state_handlers[state] = func
            return func

        if len(args) == 1 and callable(args[0]):
            _state = None
            return decorator(args[0])
        else:
            _state = args[0]
            return decorator

    async def to_state(self, user: 'User', component: Union[str, 'StateComponent'], *, reset: bool = False):
        user.state.to(component, reset=reset)
        await user.save()
        await self.to_current_state(user)

    async def to_current_state(self, user: 'User'):
        await self.state_handlers[user.state.current.name](user)

    callback_query = _event_wrapper(events.CallbackQuery)
    new_message = _event_wrapper(events.NewMessage)

    # initialization methods

    @staticmethod
    def setup_logging(level=logging.INFO):
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]', level=level)

    async def sign_in(self, *args, **kwargs):
        raise NotImplementedError('sign_in is not supported')

    # noinspection PyMethodOverriding
    async def connect(self):
        await super().connect()
        self.me = await super().sign_in(bot_token=self.bot_token)
        for c in self._after_sign_in_callbacks:
            c()
        self._after_sign_in_callbacks = []
        return self

    async def run_until_disconnected(self):
        await self._run_until_disconnected()

    async def run(self):
        if self.user_model:
            from fox_orm import FoxOrm
            await FoxOrm.connect()
        await self.connect()
        await self.run_until_disconnected()

    def run_sync(self, use_aiorun=None):
        if use_aiorun is None:
            use_aiorun = bool(aiorun)
        if use_aiorun and not aiorun:
            raise ValueError('aiorun is not installed')
        if use_aiorun:
            aiorun.run(self.run(), loop=self.loop)
        else:
            self.loop.run_until_complete(self.run())
