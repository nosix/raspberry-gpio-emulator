from collections import Sequence

from . import __version__
from .PIN import PIN
from .launcher import ui
from .task import SyncTask

VERSION = __version__

RPI_INFO = {
    'MANUFACTURER': 'Sony',
    'P1_REVISION': 3,
    'REVISION': '900092',
    'PROCESSOR': 'BCM2835',
    'RAM': '512M',
    'TYPE': 'Zero'
}

LOW = 0
HIGH = 1

OUT = PIN.OUT
IN = PIN.IN

BOARD = 10
BCM = 11

PUD_OFF = PIN.PUD_OFF
PUD_UP = PIN.PUD_UP
PUD_DOWN = PIN.PUD_DOWN

RISING = PIN.RISING
FALLING = PIN.FALLING
BOTH = PIN.BOTH

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


def __check_event(event):
    # type: (int) -> None
    assert event in [RISING, FALLING, BOTH], 'Event must be set to RISING, FALLING or BOTH'


def __to_channel(channel_or_pin):
    # type: (int) -> int
    return __PINs[channel_or_pin - 1] if __setmode == BOARD else channel_or_pin


def __change_gpio_in(channel):
    # type: (int) -> None
    pin = __pins_dict[channel]
    pin.is_on = not pin.is_on
    pin.push_event(RISING if pin.is_on else FALLING)
    ui.change_gpio_in(channel, pin.is_on)


def setmode(mode):
    # type: (int) -> None
    global __setmode
    __setmode = mode


def setwarnings(flag):
    # type: (bool) -> None
    print('setwarnings(%s)' % flag)


def setup(channel, state, initial=-1, pull_up_down=-1):
    # type: (int or Sequence[int], int, int, int) -> None
    __check_mode()

    if isinstance(channel, Sequence):
        for c in channel:
            __setup(__to_channel(c), state, initial, pull_up_down)
    else:
        __setup(__to_channel(channel), state, initial, pull_up_down)


def __setup(channel, state, initial=-1, pull_up_down=-1):
    # type: (int, int, int, int) -> None

    global __pins_dict

    assert channel in __GPIO_names, 'GPIO %d does not exist' % channel
    assert channel not in __pins_dict, 'GPIO is already setup'

    if state == OUT:
        pin = PIN(channel, "OUT")
        pin.is_on = (initial == HIGH)
        __pins_dict[channel] = pin
        ui.change_gpio_out(channel, pin.is_on)

    elif state == IN:
        pin = PIN(channel, "IN")
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


def output(channel, outmode):
    # type: (int or Sequence[int], int or bool or Sequence[int] or Sequence[bool]) -> None
    __check_mode()

    if isinstance(channel, Sequence):
        def zip_outmode():
            # type: () -> Sequence[tuple]
            if isinstance(outmode, Sequence):
                assert len(channel) == len(outmode)
                return zip(channel, outmode)
            else:
                return zip(channel, [outmode] * len(channel))

        for (c, m) in zip_outmode():
            __output(__to_channel(c), m)
    else:
        __output(__to_channel(channel), outmode)


def __output(channel, outmode):
    # type: (int, int or bool) -> None
    __check_channel(channel)

    pin = __pins_dict[channel]

    if isinstance(outmode, bool):
        outmode = HIGH if outmode else LOW

    assert pin.mode == 'OUT', 'GPIO must be setup as OUT'
    assert outmode in [LOW, HIGH], 'Output must be set to HIGH/LOW'

    pin.is_on = (outmode == HIGH)
    ui.change_gpio_out(channel, pin.is_on)


def input(channel):
    # type: (int) -> bool
    __check_mode()

    channel = __to_channel(channel)

    __check_channel(channel)

    ui.update(__change_gpio_in)

    pin = __pins_dict[channel]

    return pin.is_on


def cleanup(channel=None):
    # type: (int or Sequence[int]) -> None

    if channel is None:
        for c in __GPIO_names:
            __cleanup(c)
    elif isinstance(channel, Sequence):
        for c in channel:
            __cleanup(__to_channel(c))
    else:
        __cleanup(__to_channel(channel))


def __cleanup(channel):
    # type: (int) -> None

    global __pins_dict

    if channel in __pins_dict:
        del __pins_dict[channel]
    ui.cleanup(channel)


def wait_for_edge(channel, event, timeout=None):
    # type: (int, int, int) -> int or None
    __check_mode()

    pin_or_channel = channel
    channel = __to_channel(channel)

    __check_channel(channel)
    __check_event(event)

    pin = __pins_dict[channel]
    pin.start_monitor()

    def detect_event():
        ui.update(__change_gpio_in)
        if pin.has_event():
            if event == BOTH or pin.pop_event() == event:
                return True
        return False

    task = SyncTask(detect_event)
    task.start(timeout)
    try:
        while task.alive():
            if task.do_task():
                return pin_or_channel
        return None
    finally:
        pin.stop_monitor()


def add_event_detect(channel, event, callback=None):
    # type: (int, int) -> None
    __check_mode()

    channel = __to_channel(channel)

    __check_channel(channel)
    __check_event(event)

    pin = __pins_dict[channel]
    pin.add_event_detect(event, callback)


def event_detected(channel):
    # type: (int) -> bool
    __check_mode()

    channel = __to_channel(channel)

    __check_channel(channel)

    ui.update(__change_gpio_in)

    pin = __pins_dict[channel]
    return pin.event_detected()


def remove_event_detect(channel):
    # type: (int) -> None
    __check_mode()

    channel = __to_channel(channel)

    __check_channel(channel)

    pin = __pins_dict[channel]
    pin.remove_event_detect()
