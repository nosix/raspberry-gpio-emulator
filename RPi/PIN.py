class PIN:
    def __init__(self, mode, pull_up_down="PUD_OFF"):
        # type: (str, str) -> None
        self.mode = mode  # IN/OUT/NONE
        self.is_on = False
        self.pull_up_down = pull_up_down  # PUD_UP/PUD_DOWN/PUD_OFF
