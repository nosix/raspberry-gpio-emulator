def main():
    import RPi.GPIO as GPIO
    import time

    try:
        GPIO.setmode(GPIO.BOARD)

        GPIO.setwarnings(False)

        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(13, GPIO.IN)
        GPIO.setup(16, GPIO.OUT)

        while True:
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(11, 0)
            GPIO.output(16, True)
            time.sleep(1)
            GPIO.output(12, GPIO.LOW)
            GPIO.output(11, 1)
            GPIO.output(16, False)
            time.sleep(1)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    main()
