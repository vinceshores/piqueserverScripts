from piqueparser.piqueargsexception import PiqueArgsException, StopParsingException
from abc import abstractmethod, ABCMeta


class BaseCommand(metaclass=ABCMeta):
    name = property(lambda self: self._name)
    usage = property(lambda self: self._usage)

    def __init__(self, function, usage, name=None):
        self._name = name if name is not None else function.__name__
        self._function = function
        self._usage = usage

    def __call__(self, connection, *args):
        return self.run(connection, args)

    def run(self, connection, args):
        try:
            return self.parse_args(connection, list(args), {})
        except PiqueArgsException as e:
            return e.cls.usage
        except StopParsingException as e:
            return e.msg

    @abstractmethod
    def parse_args(self, connection, args, context):
        pass
