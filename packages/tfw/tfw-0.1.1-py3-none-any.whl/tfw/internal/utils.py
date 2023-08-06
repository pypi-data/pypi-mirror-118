import inspect
import re
from string import ascii_letters, digits
from types import FunctionType
from typing import Optional, Iterable, Type

from telethon.errors import AlreadyInConversationError
from telethon.events import StopPropagation
from telethon.tl import types

from tfw.models import User as UserModel

COMMAND_ALPHABET = set(ascii_letters + digits + '_')
MAX_COMMAND_LENGTH = 32
MIN_COMMAND_LENGTH = 1
INVALID_COMMAND_MESSAGE = f'command must consist of digits, underscore or Latin letters; ' \
                          f'length must be in [{MIN_COMMAND_LENGTH};{MAX_COMMAND_LENGTH}] '


def fullmatch_pattern(pattern: Optional[str]):
    if not isinstance(pattern, str):
        return
    if not pattern.startswith('^'):
        pattern = '^' + pattern
    if not pattern.endswith('$'):
        pattern = pattern + '$'
    return pattern


def is_correct_command(cmd: str) -> bool:
    return MIN_COMMAND_LENGTH <= len(cmd) <= MAX_COMMAND_LENGTH and \
           all(char in COMMAND_ALPHABET for char in cmd)


def build_regexp(commands: Iterable[str], username: str) -> re.Pattern:
    return re.compile(f'^/({"|".join(commands)})(@{username})?', flags=re.IGNORECASE)


def annotation_to_str(annotation: type) -> str:
    if annotation in {int, str, float, bool}:
        return annotation.__name__
    elif issubclass(annotation, UserModel):
        return 'User'
    elif annotation in {types.User, types.InputUser, types.InputPeerUser}:
        return 'User'
    else:
        raise ValueError(f'unknown annotation: {annotation}')


def validate_error_for_handler(exc: Type[Exception]):
    if exc in {AlreadyInConversationError, StopPropagation}:
        raise ValueError(f"Can't handle internal Telethon exception {exc.__qualname__}")
    if not isinstance(exc, type) or not issubclass(exc, Exception):
        raise ValueError("Can't handle objects or not Exception subclasses")


async def call_maybe_async(func: FunctionType, *args, **kwargs):
    res = func(*args, **kwargs)
    if inspect.iscoroutinefunction(func):
        res = await res
    return res
