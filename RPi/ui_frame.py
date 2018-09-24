from tkinter import *
from tkinter.font import *


class Frame:
    IS_VERTICAL = False

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

    def __init__(self, font_size=12):
        # type: (int) -> None
        self.__root = Tk()
        self.__style = {
            'font': Font(name='TkFixedFont', size=font_size, exists=True, root=self.__root),
            'width': 6,
            'height': 2
        }
        self.__gpio_btn_dict = {}
        self.__update = lambda: None
        self.__toggle = lambda channel: None

    def close(self):
        self.__root.quit()

    def __new_3v3_label(self, row, column):
        # type: (int, int) -> None
        Label(self.__root, text="3V3", fg=Frame.COLOR_3V3, **self.__style).grid(row=row, column=column, padx=(0, 0))

    def __new_5v_label(self, row, column):
        # type: (int, int) -> None
        Label(self.__root, text="5V", fg=Frame.COLOR_5V, **self.__style).grid(row=row, column=column, padx=(0, 0))

    def __new_gnd_label(self, row, column):
        # type: (int, int) -> None
        Label(self.__root, text="GND", fg=Frame.COLOR_GND, **self.__style).grid(row=row, column=column, padx=(0, 0))

    def __new_id_sc_label(self, row, column):
        # type: (int, int) -> None
        Label(self.__root, text="ID_SC", fg=Frame.COLOR_DISABLE, **self.__style).grid(row=row, column=column,
                                                                                      padx=(0, 0))

    def __new_gpio_button(self, row, column, channel):
        # type: (int, int, int) -> Label
        btn = Label(self.__root, fg=Frame.COLOR_DISABLE, **self.__style)
        btn.grid(row=row, column=column, padx=Frame.PADDING, pady=Frame.PADDING)
        self.__set_text(btn, channel)
        return btn

    def __populate(self, widget, row, col):
        if widget == Frame.W_TYPE_GND:
            self.__new_gnd_label(row, col)
        elif widget == Frame.W_TYPE_3V3:
            self.__new_3v3_label(row, col)
        elif widget == Frame.W_TYPE_5V:
            self.__new_5v_label(row, col)
        elif widget == Frame.W_TYPE_ID_SC:
            self.__new_id_sc_label(row, col)
        else:
            self.__gpio_btn_dict[widget] = self.__new_gpio_button(row, col, widget)

    def run(self, update, toggle, close):
        self.__root.title("GPIO EMULATOR")
        self.__root.protocol("WM_DELETE_WINDOW", close)
        self.__update = update
        self.__toggle = toggle

        widgets = [
            [
                Frame.W_TYPE_3V3,  # 1
                2,  # 3
                3,  # 5
                4,  # 7
                Frame.W_TYPE_GND,  # 9
                17,  # 11
                27,  # 13
                22,  # 15
                Frame.W_TYPE_3V3,  # 17
                10,  # 19
                9,  # 21
                11,  # 23
                Frame.W_TYPE_GND,  # 25
                Frame.W_TYPE_ID_SC,  # 27
                5,  # 29
                6,  # 31
                13,  # 33
                19,  # 35
                26,  # 37
                Frame.W_TYPE_GND  # 39
            ],
            [
                Frame.W_TYPE_5V,  # 2
                Frame.W_TYPE_5V,  # 4
                Frame.W_TYPE_GND,  # 6
                14,  # 8
                15,  # 10
                18,  # 12
                Frame.W_TYPE_GND,  # 14
                23,  # 16
                24,  # 18
                Frame.W_TYPE_GND,  # 20
                25,  # 22
                8,  # 24
                7,  # 26
                Frame.W_TYPE_ID_SC,  # 28
                Frame.W_TYPE_GND,  # 30
                12,  # 32
                Frame.W_TYPE_GND,  # 34
                16,  # 36
                20,  # 38
                21  # 40
            ]
        ]

        for i in range(len(widgets)):
            for j in range(len(widgets[i])):
                widget = widgets[i][j]
                if Frame.IS_VERTICAL:
                    self.__populate(widget, j, i)
                else:
                    self.__populate(widget, len(widgets) - i, j)

        self.__root.after(100, self.__update)
        self.__root.mainloop()

    def update(self):
        self.__root.after(100, self.__update)

    @staticmethod
    def __set_text(btn, channel, value='-'):
        # type: (Label, int, str) -> None
        btn['text'] = 'GPIO%02d\n%s' % (channel, value)

    @staticmethod
    def __set_state(btn, is_high, change_relief=True):
        # type: (Label, bool, bool) -> None
        if is_high:
            btn.configure(fg=Frame.COLOR_3V3)
            if change_relief:
                btn.configure(relief=RAISED)
        else:
            btn.configure(fg=Frame.COLOR_GND)
            if change_relief:
                btn.configure(relief=SUNKEN)

    def cleanup(self, channel):
        # type: (int) -> None
        btn = self.__gpio_btn_dict[channel]
        btn.configure(fg=Frame.COLOR_DISABLE)
        btn.configure(relief=FLAT)
        btn.bind('<Button-1>', lambda e: None)
        self.__set_text(btn, channel)

    def change_gpio_out(self, channel, is_high):
        # type: (int, bool) -> None
        btn = self.__gpio_btn_dict[channel]
        btn.configure(relief=FLAT)
        self.__set_state(btn, is_high, False)
        self.__set_text(btn, channel, 'OUT')

    def bind_gpio_in(self, channel, is_high):
        # type: (int, bool) -> None
        btn = self.__gpio_btn_dict[channel]
        btn.bind('<Button-1>', lambda e: self.__toggle(channel))
        self.__set_state(btn, is_high)
        self.__set_text(btn, channel, 'IN')

    def change_gpio_in(self, channel, is_high):
        # type: (int, bool) -> None
        btn = self.__gpio_btn_dict[channel]
        self.__set_state(btn, is_high)


def create_ui():
    return Frame()
