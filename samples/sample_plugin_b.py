import RPi


class Plugin(RPi.Plugin):
    def change_gpio_in(self, chanel, is_high):
        print('* change_gpio_in(%d,%d)' % (chanel, is_high))


def create_plugin():
    return Plugin()
