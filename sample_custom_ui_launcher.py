# python sample_custom_ui_launcher.py --ui sample_custom_ui


def main():
    import RPi.GPIO as GPIO
    import time

    try:
        GPIO.setmode(GPIO.BCM)

        GPIO.setwarnings(False)

        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(27, GPIO.IN)

        while True:
            time.sleep(1)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    main()
