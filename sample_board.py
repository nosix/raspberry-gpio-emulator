def main():
    import RPi.GPIO as GPIO
    import time

    try:
        GPIO.setmode(GPIO.BOARD)

        GPIO.setwarnings(False)

        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(13, GPIO.IN)

        while True:
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(11, GPIO.LOW)
            time.sleep(1)
            GPIO.output(12, GPIO.LOW)
            GPIO.output(11, GPIO.HIGH)
            time.sleep(1)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    main()
