import logging
from tkinter import *
from tkinter.font import *

from .Pipe import Pipe

_logger = logging.getLogger('RPi.UIServer')  # type: logging.Logger


class UI:
    IS_VERTICAL = False

    FONT_SIZE = 12
    PADDING = 2

    COLOR_DISABLE = 'gray'
    COLOR_GND = 'black'
    COLOR_3V3 = 'dark orange'
    COLOR_5V = 'red'

    # W_TYPE_GPIO >= 0
    W_TYPE_GND = -1
    W_TYPE_3V3 = -2
    W_TYPE_5V = -3
    W_TYPE_ID_SC = -4

    def __init__(self, pipe):
        # type: (Pipe) -> None
        self.__pipe = pipe
        self.__root = Tk()
        self.__style = {
            'font': Font(name='TkFixedFont', size=UI.FONT_SIZE, exists=True, root=self.__root),
            'width': 6,
            'height': 2
        }
        self.__gpio_btn_dict = {}
        self.__run()

    def __close(self):
        self.__root.quit()
        self.__pipe.write_bytes([Pipe.CMD_EXIT])
        self.__pipe.close()

    def __new_3v3_label(self, row, column):
        # type: (int, int) -> None
        Label(self.__root, text="3V3", fg=UI.COLOR_3V3, **self.__style).grid(row=row, column=column, padx=(0, 0))

    def __new_5v_label(self, row, column):
        # type: (int, int) -> None
        Label(self.__root, text="5V", fg=UI.COLOR_5V, **self.__style).grid(row=row, column=column, padx=(0, 0))

    def __new_gnd_label(self, row, column):
        # type: (int, int) -> None
        Label(self.__root, text="GND", fg=UI.COLOR_GND, **self.__style).grid(row=row, column=column, padx=(0, 0))

    def __new_id_sc_label(self, row, column):
        # type: (int, int) -> None
        Label(self.__root, text="ID_SC", fg=UI.COLOR_DISABLE, **self.__style).grid(row=row, column=column, padx=(0, 0))

    def __new_gpio_button(self, row, column, channel):
        # type: (int, int, int) -> Label
        btn = Label(self.__root, fg=UI.COLOR_DISABLE, **self.__style)
        btn.grid(row=row, column=column, padx=UI.PADDING, pady=UI.PADDING)
        self.__set_text(btn, channel)
        return btn

    def __populate(self, widget, row, col):
        if widget == UI.W_TYPE_GND:
            self.__new_gnd_label(row, col)
        elif widget == UI.W_TYPE_3V3:
            self.__new_3v3_label(row, col)
        elif widget == UI.W_TYPE_5V:
            self.__new_5v_label(row, col)
        elif widget == UI.W_TYPE_ID_SC:
            self.__new_id_sc_label(row, col)
        else:
            self.__gpio_btn_dict[widget] = self.__new_gpio_button(row, col, widget)

    def __run(self):
        self.__root.title("GPIO EMULATOR")
        self.__root.protocol("WM_DELETE_WINDOW", self.__close)

        widgets = [
            [
                UI.W_TYPE_3V3,  # 1
                2,  # 3
                3,  # 5
                4,  # 7
                UI.W_TYPE_GND,  # 9
                17,  # 11
                27,  # 13
                22,  # 15
                UI.W_TYPE_3V3,  # 17
                10,  # 19
                9,  # 21
                11,  # 23
                UI.W_TYPE_GND,  # 25
                UI.W_TYPE_ID_SC,  # 27
                5,  # 29
                6,  # 31
                13,  # 33
                19,  # 35
                26,  # 37
                UI.W_TYPE_GND  # 39
            ],
            [
                UI.W_TYPE_5V,  # 2
                UI.W_TYPE_5V,  # 4
                UI.W_TYPE_GND,  # 6
                14,  # 8
                15,  # 10
                18,  # 12
                UI.W_TYPE_GND,  # 14
                23,  # 16
                24,  # 18
                UI.W_TYPE_GND,  # 20
                25,  # 22
                8,  # 24
                7,  # 26
                UI.W_TYPE_ID_SC,  # 28
                UI.W_TYPE_GND,  # 30
                12,  # 32
                UI.W_TYPE_GND,  # 34
                16,  # 36
                20,  # 38
                21  # 40
            ]
        ]

        for i in range(len(widgets)):
            for j in range(len(widgets[i])):
                widget = widgets[i][j]
                if UI.IS_VERTICAL:
                    self.__populate(widget, j, i)
                else:
                    self.__populate(widget, len(widgets) - i, j)

        self.__root.after(100, self.__update)
        self.__root.mainloop()

    def __toggle(self, channel):
        # type: (int) -> None
        self.__pipe.write_bytes([Pipe.CMD_CHANGE_GPIO_IN, channel])

    def __handle_buffer(self, buf):
        # type: (bytearray) -> None
        cmd = buf.pop(0)
        if cmd == Pipe.CMD_CLEANUP:
            print("UIServer::cleanup()")
            self.cleanup()
        else:
            channel = buf.pop(0)
            is_on = buf.pop(0)
            # TODO: if channel or is_on can't get, push back to buffer.
            if cmd == Pipe.CMD_CHANGE_GPIO_OUT:
                _logger.debug("change_gpio_out(%d,%d)" % (channel, is_on))
                self.change_gpio_out(channel, is_on == 1)
            elif cmd == Pipe.CMD_BIND_GPIO_IN:
                _logger.debug("bind_gpio_in(%d,%d)" % (channel, is_on))
                self.bind_gpio_in(channel, is_on == 1)
            elif cmd == Pipe.CMD_CHANGE_GPIO_IN:
                _logger.debug("change_gpio_in(%d,%d)" % (channel, is_on))
                self.change_gpio_in(channel, is_on == 1)
            else:
                raise AssertionError('Illegal command value (%d)' % cmd)

    def __update(self):
        self.__root.after(100, self.__update)

        buf = bytearray()
        while True:
            data = self.__pipe.read_bytes()
            if not data:
                break
            buf.extend(data)
            while len(buf) > 0:
                self.__handle_buffer(buf)

    @staticmethod
    def __set_text(btn, channel, value='-'):
        # type: (Label, channel, str) -> None
        btn['text'] = 'GPIO%02d\n%s' % (channel, value)

    @staticmethod
    def __set_state(btn, is_on, change_relief=True):
        # type: (Label, bool) -> None
        if is_on:
            btn.configure(fg=UI.COLOR_3V3)
            if change_relief:
                btn.configure(relief=RAISED)
        else:
            btn.configure(fg=UI.COLOR_GND)
            if change_relief:
                btn.configure(relief=SUNKEN)

    def cleanup(self):
        # type: () -> None
        for channel, btn in self.__gpio_btn_dict.items():
            btn.configure(fg=UI.COLOR_DISABLE)
            btn.configure(relief=FLAT)
            btn.bind('<Button-1>', lambda e: None)
            self.__set_text(btn, channel)

    def change_gpio_out(self, channel, is_on):
        # type: (int, bool) -> None
        btn = self.__gpio_btn_dict[channel]
        btn.configure(relief=FLAT)
        self.__set_state(btn, is_on, False)
        self.__set_text(btn, channel, 'OUT')

    def bind_gpio_in(self, channel, is_on):
        # type: (int, bool) -> None
        btn = self.__gpio_btn_dict[channel]
        btn.bind('<Button-1>', lambda e: self.__toggle(channel))
        self.__set_state(btn, is_on)
        self.__set_text(btn, channel, 'IN')

    def change_gpio_in(self, channel, is_on):
        # type: (int, bool) -> None
        btn = self.__gpio_btn_dict[channel]
        self.__set_state(btn, is_on)
