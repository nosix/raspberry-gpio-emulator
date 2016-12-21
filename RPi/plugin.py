class Plugin:
    def cleanup(self, channel):
        # type: (int) -> None
        pass

    def change_gpio_out(self, chanel, is_high):
        # type: (int, bool) -> None
        pass

    def bind_gpio_in(self, chanel, is_high):
        # type: (int, bool) -> None
        pass

    def change_gpio_in(self, chanel, is_high):
        # type: (int, bool) -> None
        pass
