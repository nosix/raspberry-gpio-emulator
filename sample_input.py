def main():
    import RPi.GPIO as GPIO
    import time

    try:
        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        while GPIO.input(10) == GPIO.LOW:
            time.sleep(0.1)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    main()
