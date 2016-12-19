def main():
    import RPi.GPIO as GPIO
    import time
    import traceback

    try:
        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        GPIO.setup(4, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(26, GPIO.IN)

        while True:
            if not GPIO.input(23):
                GPIO.output(4, GPIO.HIGH)
                GPIO.output(17, GPIO.HIGH)
                time.sleep(1)

            if GPIO.input(15):
                GPIO.output(18, GPIO.HIGH)
                GPIO.output(21, GPIO.HIGH)
                time.sleep(1)

            if GPIO.input(24):
                GPIO.output(18, GPIO.LOW)
                GPIO.output(21, GPIO.LOW)
                time.sleep(1)

            if GPIO.input(26):
                GPIO.output(4, GPIO.LOW)
                GPIO.output(17, GPIO.LOW)
                time.sleep(1)

    except Exception:
        traceback.print_exc()
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)
    main()
