from .PIN import PIN
from .TypeChecker import type_assert
from .launcher import ui

LOW = 0
HIGH = 1
OUT = 2
IN = 3
PUD_OFF = 4
PUD_DOWN = 5
PUD_UP = 6
BCM = 7

__GPIO_names = {
    2, 3, 4, 17, 27, 22, 10, 9, 11, 5, 6, 13, 19, 26,
    14, 15, 18, 23, 24, 25, 8, 7, 12, 16, 20, 21}

__setmode_done = False
__pins_dict = {}


def __check_mode():
    assert __setmode_done, 'Setup your GPIO mode. Must be set to BCM'


def __check_channel(channel):
    # type: (int) -> None
    assert channel in __pins_dict, 'GPIO must be setup before used'


def __change_gpio_in(channel):
    # type: (int) -> None
    pin = __pins_dict[channel]
    pin.is_on = not pin.is_on
    ui.change_gpio_in(channel, pin.is_on)


@type_assert(int)
def setmode(mode):
    # type: (int) -> None
    if mode == BCM:
        global __setmode_done
        __setmode_done = True


@type_assert(bool)
def setwarnings(flag):
    # type: (bool) -> None
    print('setwarnings(%s)' % flag)


@type_assert(int, int, int, int)
def setup(channel, state, initial=-1, pull_up_down=-1):
    # type: (int, int, int, int) -> None
    __check_mode()

    global __pins_dict

    assert channel in __GPIO_names, 'GPIO %d does not exist' % channel
    assert channel not in __pins_dict, 'GPIO is already setup'

    if state == OUT:
        pin = PIN("OUT")
        pin.is_on = (initial == HIGH)
        __pins_dict[channel] = pin
        ui.change_gpio_out(channel, pin.is_on)

    elif state == IN:
        pin = PIN("IN")
        if pull_up_down == PUD_UP:
            pin.pull_up_down = "PUD_UP"
            pin.is_on = True
        elif pull_up_down == PUD_DOWN:
            pin.pull_up_down = "PUD_DOWN"
            pin.is_on = False
        else:
            pin.pull_up_down = "PUD_OFF"
            pin.is_on = False
        __pins_dict[channel] = pin
        ui.bind_gpio_in(channel, pin.is_on)


@type_assert(int, int)
def output(channel, outmode):
    # type: (int, int) -> None
    __check_mode()
    __check_channel(channel)

    pin = __pins_dict[channel]

    assert pin.mode == 'OUT', 'GPIO must be setup as OUT'
    assert outmode in [LOW, HIGH], 'Output must be set to HIGH/LOW'

    pin.is_on = (outmode == HIGH)
    ui.change_gpio_out(channel, pin.is_on)


@type_assert(int)
def input(channel):
    # type: (int) -> bool
    __check_mode()
    __check_channel(channel)

    ui.update(__change_gpio_in)

    pin = __pins_dict[channel]

    assert pin.mode == "IN", 'GPIO must be setup as IN'

    return pin.is_on


@type_assert()
def cleanup():
    # type: () -> None
    global __setmode_done
    global __pins_dict
    __setmode_done = False
    __pins_dict.clear()
    ui.cleanup()
