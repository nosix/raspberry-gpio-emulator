from .PIN import PIN
from .TypeChecker import type_assert
from .launcher import ui

LOW = 0
HIGH = 1

OUT = 0
IN = 1

BOARD = 10
BCM = 11

PUD_OFF = 20
PUD_UP = 21
PUD_DOWN = 22

# 0 is GND, 3V3, 5V or ID_SC
__PINs = [
    0, 0,
    2, 0,
    3, 0,
    4, 14,
    0, 15,
    17, 18,
    27, 0,
    22, 23,
    0, 24,
    10, 0,
    9, 25,
    11, 8,
    0, 7,
    0, 0,
    5, 0,
    6, 12,
    13, 0,
    19, 16,
    26, 20,
    0, 21
]

__GPIO_names = set(__PINs)
__GPIO_names.remove(0)

__setmode = 0
__pins_dict = {}


def __check_mode():
    assert __setmode in [BOARD, BCM], 'Setup your GPIO mode. Must be set to BOARD or BCM'


def __check_channel(channel):
    # type: (int) -> None
    assert channel in __pins_dict, 'GPIO must be setup before used'


def __to_channel(channel_or_pin):
    # type: (int) -> int
    return __PINs[channel_or_pin - 1] if __setmode == BOARD else channel_or_pin


def __change_gpio_in(channel):
    # type: (int) -> None
    pin = __pins_dict[channel]
    pin.is_on = not pin.is_on
    ui.change_gpio_in(channel, pin.is_on)


@type_assert(int)
def setmode(mode):
    # type: (int) -> None
    if mode in [BOARD, BCM]:
        global __setmode
        __setmode = mode


@type_assert(bool)
def setwarnings(flag):
    # type: (bool) -> None
    print('setwarnings(%s)' % flag)


@type_assert(int, int, int, int)
def setup(channel, state, initial=-1, pull_up_down=-1):
    # type: (int, int, int, int) -> None
    __check_mode()

    global __pins_dict

    channel = __to_channel(channel)

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

    channel = __to_channel(channel)

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

    channel = __to_channel(channel)

    __check_channel(channel)

    ui.update(__change_gpio_in)

    pin = __pins_dict[channel]

    assert pin.mode == "IN", 'GPIO must be setup as IN'

    return pin.is_on


@type_assert()
def cleanup():
    # type: () -> None
    global __setmode
    global __pins_dict
    __setmode = 0
    __pins_dict.clear()
    ui.cleanup()
