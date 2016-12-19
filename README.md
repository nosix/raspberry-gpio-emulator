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
    - initial : GPIO.LOW or GPIO.HIGH (option)
    - pull_up_down : GPIO.PUD_OFF, GPIO.PUD_DOWN or GPIO.PUD_UP (option)
- GPIO.output(channel, outmode)
    - channel : int or Sequence[int]
    - outmode : GPIO.LOW, GPIO.HIGH or Sequence[GPIO.LOW or GPIO.HIGH]
- GPIO.input(channel)
    - channel : int
- GPIO.cleanup(channel)
    - channel : int or Sequence[int] (option)

# Usage

Documentation of raspberry-gpio-python:
- [RPi.GPIO module basics](https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/)
- [Outputs](https://sourceforge.net/p/raspberry-gpio-python/wiki/Outputs/)

Sample code:
- [sample_board.py](https://github.com/nosix/raspberry-gpio-emulator/blob/master/sample_board.py)
- [sample_bcm.py](https://github.com/nosix/raspberry-gpio-emulator/blob/master/sample_bcm.py)

# Credit

This project based on [Pi GPIO Emulator](https://sourceforge.net/projects/pi-gpio-emulator/).

- [Roderick Vella](https://roderickvella.wordpress.com/2016/06/28/raspberry-pi-gpio-emulator/)
- 2016
- [Pi GPIO Emulator](https://sourceforge.net/projects/pi-gpio-emulator/)
- This project extends base design, but it change usage and implementation.
