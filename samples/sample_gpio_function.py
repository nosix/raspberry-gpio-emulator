def main():
    import RPi.GPIO as GPIO

    try:
        print('UNKNOWN:%d' % GPIO.UNKNOWN)
        print('SERIAL:%d' % GPIO.SERIAL)
        print('SPI:%d' % GPIO.SPI)
        print('I2C:%d' % GPIO.I2C)
        print('HARD_PWM:%d' % GPIO.HARD_PWM)

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(3, GPIO.OUT)

        for pin in range(1, 41):
            try:
                print('%02d: %d' % (pin, GPIO.gpio_function(pin)))
            except ValueError as ex:
                print(ex)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    import logging

    logging.basicConfig(level=logging.DEBUG)

    main()
