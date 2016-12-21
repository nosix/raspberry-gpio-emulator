from collections import Sequence

from . import __version__
from . import pin as pins
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

OUT = pins.OUT
IN = pins.IN

BOARD = 10
BCM = 11

PUD_OFF = pins.PUD_OFF
PUD_UP = pins.PUD_UP
PUD_DOWN = pins.PUD_DOWN

RISING = pins.RISING
FALLING = pins.FALLING
BOTH = pins.BOTH

SERIAL = pins.SERIAL
SPI = pins.SPI
I2C = pins.I2C
HARD_PWM = pins.HARD_PWM

UNKNOWN = -1

# pin -> GPIO (0 is GND, 3V3, 5V or ID_SC)
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

__gpio_function = {
    2: IN,
    3: IN,
    4: IN,
    14: SERIAL,
    15: SERIAL,
    17: IN,
    18: IN,
    27: IN,
    22: IN,
    23: IN,
    24: IN,
    10: IN,
    9: IN,
    25: IN,
    11: IN,
    8: IN,
    7: IN,
    5: IN,
    6: IN,
    12: IN,
    13: IN,
    19: IN,
    16: IN,
    26: IN,
    20: IN,
    21: IN
}

__GPIO_names = __gpio_function.keys()

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
    pin.is_high = not pin.is_high
    pin.push_event(RISING if pin.is_high else FALLING)
    ui.change_gpio_in(channel, pin.is_high)


ui.on_change = __change_gpio_in


def setmode(mode):
    # type: (int) -> None

    if mode not in [BOARD, BCM]:
        raise ValueError('An invalid mode was passed to setmode()')

    global __setmode

    if __setmode != 0 and __setmode != mode:
        raise ValueError('A different mode has already been set!')

    __setmode = mode


def setwarnings(flag):
    # type: (bool) -> None
    print('setwarnings(%s)' % flag)


def setup(channel, state, initial=LOW, pull_up_down=PUD_OFF):
    # type: (int or Sequence[int], int, int, int) -> None
    __check_mode()

    if isinstance(channel, Sequence):
        for c in channel:
            __setup(__to_channel(c), state, initial, pull_up_down)
    else:
        __setup(__to_channel(channel), state, initial, pull_up_down)


def __setup(channel, state, initial=LOW, pull_up_down=PUD_OFF):
    # type: (int, int, int, int) -> None

    global __pins_dict

    assert channel in __GPIO_names, 'GPIO %d does not exist' % channel
    assert channel not in __pins_dict, 'GPIO is already setup'
    assert state in [OUT, IN], 'State must be set to OUT or IN'
    assert pull_up_down in [PUD_OFF, PUD_UP, PUD_DOWN], 'Pull up/down must be set to PUD_OFF, PUD_UP or PUD_DOWN'

    pin = pins.Pin(channel, state)
    __pins_dict[channel] = pin

    if state == OUT:
        pin.is_high = (initial == HIGH)
        ui.change_gpio_out(channel, pin.is_high)

    elif state == IN:
        pin.pull_up_down = pull_up_down
        pin.is_high = (pull_up_down == PUD_UP)
        ui.bind_gpio_in(channel, pin.is_high)


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

    assert pin.mode == OUT, 'GPIO must be setup as OUT'
    assert outmode in [LOW, HIGH], 'Output must be set to HIGH/LOW'

    pin.is_high = (outmode == HIGH)
    ui.change_gpio_out(channel, pin.is_high)


def input(channel):
    # type: (int) -> bool
    __check_mode()

    channel = __to_channel(channel)

    __check_channel(channel)

    pin = __pins_dict[channel]

    return pin.is_high


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


def add_event_detect(channel, event, callback=None, bouncetime=None):
    # type: (int, int) -> None
    __check_mode()

    channel = __to_channel(channel)

    __check_channel(channel)
    __check_event(event)

    pin = __pins_dict[channel]
    pin.add_event_detect(event, callback, bouncetime)


def add_event_callback(channel, callback, bouncetime=None):
    # type: (int) -> None
    __check_mode()

    channel = __to_channel(channel)

    __check_channel(channel)

    pin = __pins_dict[channel]
    pin.add_event_detect(None, callback, bouncetime)


def event_detected(channel):
    # type: (int) -> bool
    __check_mode()

    channel = __to_channel(channel)

    __check_channel(channel)

    pin = __pins_dict[channel]
    return pin.event_detected()


def remove_event_detect(channel):
    # type: (int) -> None
    __check_mode()

    channel = __to_channel(channel)

    __check_channel(channel)

    pin = __pins_dict[channel]
    pin.remove_event_detect()


def gpio_function(channel):
    __check_mode()

    channel = __to_channel(channel)

    if channel in __pins_dict:
        return __pins_dict[channel].mode
    elif channel in __gpio_function:
        return __gpio_function[channel]
    else:
        raise ValueError('The channel sent is invalid on a Raspberry Pi')


class PWM:
    def __init__(self, channel, frequency):
        # type: (int, float) -> None
        self.channel = channel
        self.__frequency = frequency  # Hz
        self.__duty_cycle = 0  # 0.0 <= duty_cycle <= 100.0

    def start(self, duty_cycle):
        # type: (float) -> None
        self.__duty_cycle = duty_cycle
        print("start() don't do anything.")

    def stop(self):
        # type: () -> None
        print("stop() don't do anything.")

    def ChangeFrequency(self, frequency):
        # type: (float) -> None
        self.__frequency = frequency

    def ChangeDutyCycle(self, duty_cycle):
        # type: (float) -> None
        self.__duty_cycle = duty_cycle
