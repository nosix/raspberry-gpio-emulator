from builtins import bytes
from io import TextIOWrapper


class Pipe:
    CMD_EXIT = 127
    CMD_CLEANUP = 126
    CMD_CHANGE_GPIO_OUT = 125
    CMD_BIND_GPIO_IN = 124
    CMD_CHANGE_GPIO_IN = 123

    def __init__(self, w_pipe, r_pipe):
        # type: (TextIOWrapper, TextIOWrapper) -> None
        self.__w_pipe = w_pipe
        self.__r_pipe = r_pipe
        self.__alive = True

    def close(self):
        # type: () -> None
        self.__w_pipe.close()
        self.__r_pipe.close()
        self.__alive = False

    def write_bytes(self, values):
        # type: ([int]) -> None
        if self.__alive:
            self.__w_pipe.write(bytes(values))
            self.__w_pipe.flush()

    def read_bytes(self):
        # type: () -> bytes or None
        if self.__alive:
            data = self.__r_pipe.read()
            return bytes(data) if data else None
        else:
            return None
