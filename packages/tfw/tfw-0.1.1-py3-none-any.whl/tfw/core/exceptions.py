from enum import Enum


class TFWInternalException(Exception):
    pass


class BadSignatureError(TFWInternalException):
    pass


class WrongUsageKind(str, Enum):
    too_many_arguments = 'too many arguments'
    not_enough_arguments = 'not enough arguments'
    failed_to_parse = 'failed to parse argument #{}'


class WrongUsageError(TFWInternalException):
    kind: WrongUsageKind
    args: list

    def __init__(self, kind, *args):
        self.args = list(args)
        self.kind = kind

    def format(self, formatter=None):
        if formatter:
            return formatter(self.kind, self.args)
        else:
            return self.kind.value.format(*self.args)
