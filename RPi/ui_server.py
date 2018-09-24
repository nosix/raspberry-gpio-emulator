import logging

from .pipe import Pipe
from .ui_frame import Frame

_logger = logging.getLogger('RPi.UIServer')  # type: logging.Logger


class UI:
    def __init__(self, pipe, frame, plugins):
        # type: (Pipe, Frame) -> None
        self.__pipe = pipe
        self.__frame = frame
        self.__plugins = plugins

    def close(self):
        self.__frame.close()
        self.__pipe.write_bytes([Pipe.CMD_EXIT])
        self.__pipe.close()

    def run(self):
        self.__frame.run(self.__update, self.__toggle, self.close)

    def __toggle(self, channel):
        # type: (int) -> None
        self.__pipe.write_bytes([Pipe.CMD_CHANGE_GPIO_IN, channel])

    def __handle_buffer(self, buf):
        # type: (bytearray) -> None
        cmd = buf.pop(0)
        if cmd == Pipe.CMD_CLEANUP:
            channel = buf.pop(0)
            # TODO: if channel can't get, push back to buffer.
            _logger.debug("cleanup(%d)" % channel)
            self.__frame.cleanup(channel)
            for p in self.__plugins:
                p.cleanup(channel)
        else:
            channel = buf.pop(0)
            is_high = buf.pop(0)
            # TODO: if channel or is_high can't get, push back to buffer.
            if cmd == Pipe.CMD_CHANGE_GPIO_OUT:
                _logger.debug("change_gpio_out(%d,%d)" % (channel, is_high))
                self.__frame.change_gpio_out(channel, is_high == 1)
                for p in self.__plugins:
                    p.change_gpio_out(channel, is_high)
            elif cmd == Pipe.CMD_BIND_GPIO_IN:
                _logger.debug("bind_gpio_in(%d,%d)" % (channel, is_high))
                self.__frame.bind_gpio_in(channel, is_high == 1)
                for p in self.__plugins:
                    p.bind_gpio_in(channel, is_high)
            elif cmd == Pipe.CMD_CHANGE_GPIO_IN:
                _logger.debug("change_gpio_in(%d,%d)" % (channel, is_high))
                self.__frame.change_gpio_in(channel, is_high == 1)
                for p in self.__plugins:
                    p.change_gpio_in(channel, is_high)
            else:
                raise AssertionError('Illegal command value (%d)' % cmd)

    def __update(self):
        try:
            self.__frame.update()

            buf = bytearray()
            while True:
                data = self.__pipe.read_bytes()
                if not data:
                    break
                buf.extend(data)
                while len(buf) > 0:
                    self.__handle_buffer(buf)
        except Exception as ex:
            self.close()
            raise ex
