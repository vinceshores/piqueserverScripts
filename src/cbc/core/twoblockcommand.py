from enum import IntEnum
from abc import abstractmethod, ABCMeta
from cbc.core.buildorclearcommand import BuildOrClearState


class _Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class ChooseStatus(IntEnum):
    CHOOSING_FIRST_BLOCK = 0
    CHOOSING_SECOND_BLOCK = 1


def two_block_command(connection, two_block_state_type):
    if isinstance(connection.state, TwoBlockState):
        connection.state = None
        return
    connection.state = two_block_state_type(connection)


class TwoBlockState(BuildOrClearState, metaclass=ABCMeta):
    CHOOSE_SECOND_MESSAGE = ''

    def __init__(self, *args, **kwargs):
        BuildOrClearState.__init__(self, *args, **kwargs)
        self._choosing = ChooseStatus.CHOOSING_FIRST_BLOCK
        self._first_point = _Point(0, 0, 0)

    @abstractmethod
    def on_apply(self, point1, point2):
        pass

    def on_block(self, x, y, z):
        point = _Point(x, y, z)
        if self._choosing == ChooseStatus.CHOOSING_FIRST_BLOCK:
            self._first_point = point
            self.player.send_chat(self.CHOOSE_SECOND_MESSAGE)
            self._choosing = ChooseStatus.CHOOSING_SECOND_BLOCK
        if self._choosing == ChooseStatus.CHOOSING_SECOND_BLOCK:
            self.on_apply(self._first_point, point)
            self.player.state = None
