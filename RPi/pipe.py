from builtins import bytes
from io import TextIOWrapper


class Pipe:
    CMD_TERMINATE = 127
    CMD_EXIT = 126
    CMD_CLEANUP = 125
    CMD_CHANGE_GPIO_OUT = 124
    CMD_BIND_GPIO_IN = 123
    CMD_CHANGE_GPIO_IN = 122

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
            self.__w_pipe.write(bytes(values + [Pipe.CMD_TERMINATE]))
            self.__w_pipe.flush()

    def read_bytes(self):
        # type: () -> bytes or None
        buf = bytearray()
        if self.__alive:
            while True:
                data = self.__r_pipe.read(1)
                if data is None:
                    return None
                if data[0] == Pipe.CMD_TERMINATE:
                    return bytes(buf)
                buf.extend(data)
        else:
            return None
