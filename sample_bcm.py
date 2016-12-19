def main():
    import RPi.GPIO as GPIO
    import time

    try:
        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(27, GPIO.IN)

        while True:
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(17, GPIO.LOW)
            time.sleep(1)
            GPIO.output(18, GPIO.LOW)
            GPIO.output(17, GPIO.HIGH)
            time.sleep(1)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    main()
