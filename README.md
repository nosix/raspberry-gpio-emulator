# raspberry-gpio-emulator

RPi.GPIO emulator

# Require

- Python 3.5

# Install

```bash
$ pip install git+https://github.com/nosix/raspberry-gpio-emulator/
```

# API

```python
import RPi.GPIO as GPIO
```

- GPIO.setmode(mode)
    - mode : GPIO.BOARD or GPIO.BCP
- GPIO.setwarnings(flag)
    - flag : bool
- GPIO.setup(channel, state, initial, pull_up_down)
    - channel : int or Sequence[int]
    - state : GPIO.OUT or GPIO.IN
    - initial (option) : GPIO.LOW or GPIO.HIGH
    - pull_up_down (option) : GPIO.PUD_OFF, GPIO.PUD_DOWN or GPIO.PUD_UP
- GPIO.output(channel, outmode)
    - channel : int or Sequence[int]
    - outmode : GPIO.LOW, GPIO.HIGH or Sequence[GPIO.LOW or GPIO.HIGH]
- GPIO.input(channel) : bool
    - channel : int
- GPIO.cleanup(channel)
    - channel (option) : int or Sequence[int]
- GPIO.wait_for_edge(channel, event, timeout) : int or None
    - channel : int
    - event : GPIO.RISING, GPIO.FALLING or GPIO.BOTH
    - timeout (option) : int or None
- GPIO.add_event_detect(channel, event, callback)
    - channel : int
    - event : GPIO.RISING, GPIO.FALLING or GPIO.BOTH
    - callback : None or function(channel)
        - channel : int
- GPIO.add_event_callback(channel, callback)
    - channel : int
    - callback : function(channel)
        - channel : int
- GPIO.remove_event_detect(channel)
    - channel : int
- GPIO.event_detected(channel) : bool
    - channel : int

# Usage

Documentation of raspberry-gpio-python:
- [RPi.GPIO module basics](https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/)
- [Outputs](https://sourceforge.net/p/raspberry-gpio-python/wiki/Outputs/)
- [Inputs](https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/)

Sample code:
- [sample_board.py](https://github.com/nosix/raspberry-gpio-emulator/blob/master/sample_board.py)
- [sample_bcm.py](https://github.com/nosix/raspberry-gpio-emulator/blob/master/sample_bcm.py)
- [sample_input.py](https://github.com/nosix/raspberry-gpio-emulator/blob/master/sample_input.py)

# Credit

This project based on [Pi GPIO Emulator](https://sourceforge.net/projects/pi-gpio-emulator/).

- [Roderick Vella](https://roderickvella.wordpress.com/2016/06/28/raspberry-pi-gpio-emulator/)
- 2016
- [Pi GPIO Emulator](https://sourceforge.net/projects/pi-gpio-emulator/)
- This project uses base design as reference, but it changes usage and implementation.
