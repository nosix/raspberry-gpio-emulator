class Counter:
    def __init__(self):
        self.count = 0

    def count_up(self, channel):
        self.count += 1
        print('GPIO%02d count=%d' % (channel, self.count))

    def __eq__(self, other):
        return self.count == other

    def __lt__(self, other):
        return self.count < other


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

        print('Press GPIO10.')

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
            print('Wait timeout.')
            channel = GPIO.wait_for_edge(10, GPIO.BOTH, timeout=1000)
            if channel is None:
                GPIO.output(26, GPIO.HIGH)
                break

        print('Press GPIO10.')

        GPIO.add_event_detect(10, GPIO.RISING)
        while not GPIO.event_detected(10):
            time.sleep(1)
        GPIO.output(5, GPIO.LOW)
        GPIO.remove_event_detect(10)

        GPIO.add_event_detect(10, GPIO.FALLING)
        while not GPIO.event_detected(10):
            time.sleep(1)
        GPIO.output(6, GPIO.LOW)
        GPIO.remove_event_detect(10)

        GPIO.add_event_detect(10, GPIO.BOTH)
        while not GPIO.event_detected(10):
            time.sleep(1)
        GPIO.output(13, GPIO.LOW)
        GPIO.remove_event_detect(10)

        def risen(ch):
            print('risen GPIO%02d' % ch)

        def fallen(ch):
            print('fallen GPIO%02d' % ch)

        GPIO.add_event_detect(10, GPIO.RISING, risen)
        while not GPIO.event_detected(10):
            time.sleep(1)
        GPIO.output(5, GPIO.HIGH)
        GPIO.remove_event_detect(10)

        GPIO.add_event_detect(10, GPIO.FALLING, fallen)
        while not GPIO.event_detected(10):
            time.sleep(1)
        GPIO.output(6, GPIO.HIGH)
        GPIO.remove_event_detect(10)

        GPIO.add_event_detect(10, GPIO.BOTH, risen)
        while not GPIO.event_detected(10):
            time.sleep(1)
        GPIO.output(13, GPIO.HIGH)
        GPIO.remove_event_detect(10)

        def changed(ch):
            print('changed GPIO%02d' % ch)

        GPIO.add_event_detect(10, GPIO.BOTH)
        GPIO.add_event_callback(10, fallen)
        GPIO.add_event_callback(10, changed)
        while not GPIO.event_detected(10):
            time.sleep(1)
        GPIO.output(26, GPIO.LOW)
        GPIO.remove_event_detect(10)

        print('Press! Press! Press!')

        counter = Counter()

        GPIO.add_event_detect(10, GPIO.RISING, callback=counter.count_up, bouncetime=100)
        GPIO.add_event_callback(10, counter.count_up, bouncetime=500)
        while counter < 10:
            time.sleep(1)
        GPIO.output(19, GPIO.LOW)
        GPIO.remove_event_detect(10)

        time.sleep(1)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    main()
