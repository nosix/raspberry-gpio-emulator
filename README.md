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

GPIO:

- setmode(mode)
    - mode : GPIO.BOARD or GPIO.BCP
- setwarnings(flag)
    - flag : bool
- setup(channel, state, initial, pull_up_down)
    - channel : int or Sequence[int]
    - state : GPIO.OUT or GPIO.IN
    - initial (option) : GPIO.LOW or GPIO.HIGH
    - pull_up_down (option) : GPIO.PUD_OFF, GPIO.PUD_DOWN or GPIO.PUD_UP
- output(channel, outmode)
    - channel : int or Sequence[int]
    - outmode : GPIO.LOW, GPIO.HIGH or Sequence[GPIO.LOW or GPIO.HIGH]
- input(channel) : bool
    - channel : int
- cleanup(channel)
    - channel (option) : int or Sequence[int]
- wait_for_edge(channel, event, timeout) : int or None
    - channel : int
    - event : GPIO.RISING, GPIO.FALLING or GPIO.BOTH
    - timeout (option) : int [millisecond]
- add_event_detect(channel, event, callback, bouncetime)
    - channel : int
    - event : GPIO.RISING, GPIO.FALLING or GPIO.BOTH
    - callback (option) : function(channel)
        - channel : int
    - bouncetime (option) : int [millisecond]
- add_event_callback(channel, callback, bouncetime)
    - channel : int
    - callback : function(channel)
        - channel : int
    - bouncetime (option) : int [millisecond]
- remove_event_detect(channel)
    - channel : int
- event_detected(channel) : bool
    - channel : int
- gpio_function(channel) : GPIO.OUT, GPIO.IN, GPIO.SERIAL, GPIO.SPI, GPIO.I2C or GPIO.HARD_PWM
    - channel : int
- PWM(channel, frequency) : GPIO.PWM
    - channel : int
    - frequency : float [Hz]

GPIO.PWM:

- start(duty_cycle)
    - duty_cycle : float [0.0..100.0]
- stop()
- ChangeFrequency(frequency)
    - frequency : float [Hz]
- ChangeDutyCycle(duty_cycle)
    - duty_cycle : float [0.0..100.0]

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
