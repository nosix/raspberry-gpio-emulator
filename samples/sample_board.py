def main():
    import RPi.GPIO as GPIO
    import time

    try:
        print(GPIO.VERSION)
        print(GPIO.RPI_INFO)

        GPIO.setmode(GPIO.BOARD)

        GPIO.setwarnings(False)

        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(13, GPIO.IN)
        GPIO.setup(15, GPIO.OUT)
        GPIO.setup([16, 18], GPIO.OUT)
        GPIO.setup((8, 10), GPIO.OUT)
        GPIO.setup([21, 19], GPIO.IN)

        GPIO.setup(3, GPIO.IN)
        GPIO.cleanup(3)

        GPIO.setup([5, 7], GPIO.OUT)
        GPIO.cleanup([5, 7])

        GPIO.setup([5, 7], GPIO.IN)
        GPIO.cleanup((5, 7))

        while True:
            GPIO.output(12, GPIO.HIGH)
            GPIO.output(11, 0)
            GPIO.output(15, True)
            GPIO.output([16, 18], not GPIO.input(16))
            GPIO.output((8, 10), [GPIO.HIGH, GPIO.LOW])
            time.sleep(1)

            GPIO.output(12, GPIO.LOW)
            GPIO.output(11, 1)
            GPIO.output(15, False)
            GPIO.output((16, 18), not GPIO.input(16))
            GPIO.output([8, 10], (GPIO.LOW, GPIO.HIGH))
            time.sleep(1)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    main()
