import inspect
import shlex
from types import FunctionType
from typing import List, Any, Union

from telethon.events import NewMessage, CallbackQuery

from . import exceptions
from .converters import CTX_DEFAULT_CONVERTERS, TEXT_DEFAULT_CONVERTERS, CONVERTERS_TYPE
from ..internal.utils import call_maybe_async


async def _convert_text_arg(event, raw_arg: str, annotation: type, text_converters: CONVERTERS_TYPE):
    for type_ in annotation.mro():
        if converter := text_converters.get(type_):
            break
    else:
        raise exceptions.BadSignatureError(f"unknown parameter annotation: {repr(annotation)}")
    try:
        only_value = True
        if isinstance(converter, FunctionType):
            converter_sig = inspect.signature(converter)
            only_value = len(converter_sig.parameters) == 1
        if only_value:
            converted_arg = await call_maybe_async(converter, raw_arg)
        else:
            converted_arg = await call_maybe_async(converter, event, raw_arg)
    except ValueError as e:
        raise ValueError(f'Could not convert {repr(raw_arg)} to {repr(annotation)}') from e
    return converted_arg


async def convert_arguments(event: Union[NewMessage.Event, CallbackQuery.Event],
                            signature: inspect.Signature,
                            parse_text: bool,
                            ctx_converters: CONVERTERS_TYPE = CTX_DEFAULT_CONVERTERS,
                            text_converters: CONVERTERS_TYPE = TEXT_DEFAULT_CONVERTERS,
                            ) -> List[Any]:
    if parse_text:
        str_args = shlex.split(event.raw_text)[1:]
    else:
        str_args = None
    positional_args = []
    str_arg_ptr = 0
    for arg in signature.parameters.values():
        # Context args:
        # (Before /) or (no / and parse_text is False)
        if arg.kind == inspect.Parameter.POSITIONAL_ONLY \
                or (arg.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD and not parse_text):
            for type_ in arg.annotation.mro():
                if converter := ctx_converters.get(type_):
                    # TODO: raise appropriate exception if conversion failed
                    converted_arg = await call_maybe_async(converter, event)
                    positional_args.append(converted_arg)
                    break
            else:
                raise exceptions.BadSignatureError(
                    f'Unknown type specified in context args: {arg.annotation}'
                )
        # TODO: unsmoke
        # Text arguments (after /)
        elif parse_text and arg.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            if str_arg_ptr == len(str_args):
                if arg.default == inspect.Parameter.empty:
                    raise exceptions.WrongUsageError(
                        exceptions.WrongUsageKind.not_enough_arguments
                    )
                else:
                    positional_args.append(arg.default)
                    continue
            raw_arg = str_args[str_arg_ptr]
            str_arg_ptr += 1
            try:
                resolved_arg = await _convert_text_arg(event, raw_arg, arg.annotation, text_converters)
            except ValueError:
                raise exceptions.WrongUsageError(
                    exceptions.WrongUsageKind.failed_to_parse,
                    str_arg_ptr
                )
            positional_args.append(resolved_arg)
        # Variable text arguments (*args after /)
        elif parse_text and arg.kind == inspect.Parameter.VAR_POSITIONAL:
            for raw_arg in str_args[str_arg_ptr:]:
                str_arg_ptr += 1
                try:
                    positional_args.append(await _convert_text_arg(event, raw_arg, arg.annotation, text_converters))
                except ValueError:
                    raise exceptions.WrongUsageError(
                        exceptions.WrongUsageKind.failed_to_parse,
                        str_arg_ptr
                    )
        else:
            raise exceptions.BadSignatureError(
                f"parameter kind {repr(arg.kind.name)} is not supported in current context"
            )
    if parse_text and str_arg_ptr != len(str_args):
        raise exceptions.WrongUsageError(exceptions.WrongUsageKind.too_many_arguments)
    return positional_args
