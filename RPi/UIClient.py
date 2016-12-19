import sys

from .Pipe import Pipe


class UI:
    def __init__(self, pipe):
        # type: (Pipe) -> None
        self.__pipe = pipe

    def __close(self):
        # type: () -> None
        self.__pipe.close()
        sys.exit(0)

    def change_gpio_out(self, channel, is_on):
        # type: (int, bool) -> None
        self.__pipe.write_bytes([Pipe.CMD_CHANGE_GPIO_OUT, channel, 1 if is_on else 0])

    def bind_gpio_in(self, channel, is_on):
        # type: (int, bool) -> None
        self.__pipe.write_bytes([Pipe.CMD_BIND_GPIO_IN, channel, 1 if is_on else 0])

    def change_gpio_in(self, channel, is_on):
        # type: (int, bool) -> None
        self.__pipe.write_bytes([Pipe.CMD_CHANGE_GPIO_IN, channel, 1 if is_on else 0])

    def cleanup(self):
        # type: () -> None
        self.__pipe.write_bytes([Pipe.CMD_CLEANUP])

    def update(self, callback):
        buf = bytearray()
        while True:
            data = self.__pipe.read_bytes()
            if not data:
                break
            buf.extend(data)
            while len(buf) > 0:
                self.__handle_buffer(buf, callback)

    def __handle_buffer(self, buf, callback):
        # type: (bytearray) -> None
        cmd = buf.pop(0)
        if cmd == Pipe.CMD_EXIT:
            self.__close()
        elif cmd == Pipe.CMD_CHANGE_GPIO_IN:
            channel = buf.pop(0)
            # TODO: if channel can't get, push back to buffer.
            callback(channel)
        else:
            raise AssertionError('Illegal command value (%d)' % cmd)
