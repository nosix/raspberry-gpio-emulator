from _thread import interrupt_main
from threading import Thread

from .pipe import Pipe


class UI:
    def __init__(self, pipe):
        # type: (Pipe) -> None
        self.__pipe = pipe
        self.__thread = Thread(target=self.__update)
        self.__alive = True
        self.__thread.start()
        self.interrupt_main_to_close = True
        self.on_change = lambda channel: None  # callback function that is called when pipe read CMD_CHANGE_GPIO_IN

    def __close(self):
        # type: () -> None
        self.__alive = False

    def change_gpio_out(self, channel, is_high):
        # type: (int, bool) -> None
        self.__pipe.write_bytes([Pipe.CMD_CHANGE_GPIO_OUT, channel, 1 if is_high else 0])

    def bind_gpio_in(self, channel, is_high):
        # type: (int, bool) -> None
        self.__pipe.write_bytes([Pipe.CMD_BIND_GPIO_IN, channel, 1 if is_high else 0])

    def change_gpio_in(self, channel, is_high):
        # type: (int, bool) -> None
        self.__pipe.write_bytes([Pipe.CMD_CHANGE_GPIO_IN, channel, 1 if is_high else 0])

    def cleanup(self, channel):
        # type: (int) -> None
        self.__pipe.write_bytes([Pipe.CMD_CLEANUP, channel])

    def __update(self):
        buf = bytearray()
        while self.__alive:
            data = self.__pipe.read_bytes()
            buf.extend(data)
            while len(buf) > 0:
                self.__handle_buffer(buf)
        self.__pipe.close()
        if self.interrupt_main_to_close:
            interrupt_main()

    def __handle_buffer(self, buf):
        # type: (bytearray) -> None
        cmd = buf.pop(0)
        if cmd == Pipe.CMD_EXIT:
            self.__close()
        elif cmd == Pipe.CMD_CHANGE_GPIO_IN:
            channel = buf.pop(0)
            # TODO: if channel can't get, push back to buffer.
            self.on_change(channel)
        else:
            raise AssertionError('Illegal command value (%d)' % cmd)
