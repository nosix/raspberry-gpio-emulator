import RPi


class Plugin(RPi.Plugin):
    def cleanup(self, channel):
        print('cleanup(%d)' % channel)

    def change_gpio_out(self, chanel, is_high):
        print('change_gpio_out(%d,%d)' % (chanel, is_high))

    def bind_gpio_in(self, chanel, is_high):
        print('bind_gpio_in(%d,%d)' % (chanel, is_high))

    def change_gpio_in(self, chanel, is_high):
        print('change_gpio_in(%d,%d)' % (chanel, is_high))


def create_plugin():
    return Plugin()
