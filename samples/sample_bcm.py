def main():
    import RPi.GPIO as GPIO
    import time

    try:
        print(GPIO.VERSION)
        print(GPIO.RPI_INFO)

        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT, initial=GPIO.HIGH)
        GPIO.setup(27, GPIO.IN)
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup([23, 24], GPIO.OUT)
        GPIO.setup((14, 15), GPIO.OUT)
        GPIO.setup([9, 10], GPIO.IN)

        GPIO.setup(2, GPIO.IN)
        GPIO.cleanup(2)

        GPIO.setup([3, 4], GPIO.OUT)
        GPIO.cleanup([3, 4])

        GPIO.setup([3, 4], GPIO.IN)
        GPIO.cleanup((3, 4))

        while True:
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(17, 0)
            GPIO.output(22, True)
            GPIO.output([23, 24], not GPIO.input(23))
            GPIO.output((14, 15), [GPIO.HIGH, GPIO.LOW])
            time.sleep(1)

            GPIO.output(18, GPIO.LOW)
            GPIO.output(17, 1)
            GPIO.output(22, False)
            GPIO.output((23, 24), not GPIO.input(23))
            GPIO.output([14, 15], (GPIO.LOW, GPIO.HIGH))
            time.sleep(1)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    main()
