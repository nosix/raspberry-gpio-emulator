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

function:
- GPIO.setmode(mode)
- GPIO.setwarnings(flag)
- GPIO.setup(channel, state, initial, pull_up_down)
- GPIO.output(channel, outmode)
- GPIO.input(channel)
- GPIO.cleanup()

mode:
- GPIO.BCP

state:
- GPIO.OUT
- GPIO.IN

initial, outmode:
- GPIO.LOW
- GPIO.HIGH

pull_up_down:
- GPIO.PUD_OFF
- GPIO.PUD_DOWN
- GPIO.PUD_UP

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
