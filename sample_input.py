def main():
    import RPi.GPIO as GPIO
    import time

    try:
        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        GPIO.setup([5, 6, 13, 19, 26], GPIO.OUT)

        GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        GPIO.setup(9, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        while GPIO.input(10) == GPIO.LOW:
            time.sleep(0.1)
        GPIO.output(5, GPIO.HIGH)

        channel = GPIO.wait_for_edge(10, GPIO.FALLING)
        if channel == 10:
            GPIO.output(6, GPIO.HIGH)

        channel = GPIO.wait_for_edge(10, GPIO.RISING)
        if channel == 10:
            GPIO.output(13, GPIO.HIGH)

        channel = GPIO.wait_for_edge(10, GPIO.BOTH)
        if channel == 10:
            GPIO.output(19, GPIO.HIGH)

        while True:
            channel = GPIO.wait_for_edge(10, GPIO.BOTH, timeout=1000)
            if channel is None:
                GPIO.output(26, GPIO.HIGH)
                break

        time.sleep(1)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    main()
