from tkinter import *


class Frame:
    def __init__(self):
        # type: () -> None
        self.__root = Tk()
        self.__update = lambda: None
        self.__toggle = lambda channel: None
        self.__widget = None

    # update:
    #   Function that you must call when you update UI.
    #   This function handle events which model sent and call update function in this class.
    # toggle:
    #   Function that you must call when state of gpio_in is changed.
    #   This function communicate to model and call change_gpio_in function in this class.
    # close:
    #   Function that you must call UI is closed.
    #   This function communicate to model and call close function in this class.
    def run(self, update, toggle, close):
        self.__root.title("GPIO EMULATOR")
        self.__root.protocol("WM_DELETE_WINDOW", close)
        self.__update = update
        self.__toggle = toggle

        self.__widget = Label(self.__root, text="GPIO IN", relief=RAISED)
        self.__widget.grid(row=0, column=0, padx=(0, 0))

        self.__root.after(100, self.__update)
        self.__root.mainloop()

    def close(self):
        self.__root.quit()

    def update(self):
        self.__root.after(100, self.__update)

    # This function is called when GPIO.cleanup() is called.
    def cleanup(self, channel):
        # type: (int) -> None
        print('cleanup(%d)' % channel)

    # This function is called when GPIO.output(channel, GPIO.HIGH/LOW) is called.
    def change_gpio_out(self, channel, is_high):
        # type: (int, bool) -> None
        print('change_gpio_out(%d,%d)' % (channel, is_high))

    # This function is called when GPIO.setup(channel, GPIO.IN) is called.
    def bind_gpio_in(self, channel, is_high):
        # type: (int, bool) -> None
        print('bind_gpio_in(%d,%d)' % (channel, is_high))
        self.__widget.bind('<Button-1>', lambda e: self.__toggle(channel))

    # This function is callback when you call toggle function.
    def change_gpio_in(self, channel, is_high):
        # type: (int, bool) -> None
        print('change_gpio_in(%d,%d)' % (channel, is_high))


def create_ui():
    return Frame()
