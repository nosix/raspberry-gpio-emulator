class PIN:
    def __init__(self, mode, pull_up_down="PUD_OFF"):
        # type: (str, str) -> None
        self.mode = mode  # IN/OUT/NONE
        self.is_on = False
        self.pull_up_down = pull_up_down  # PUD_UP/PUD_DOWN/PUD_OFF
        self.__event = []
        self.__monitor_event = False

    def has_event(self):
        # type: () -> bool
        return len(self.__event) > 0

    def pop_event(self):
        # type: () -> int
        return self.__event.pop(0)

    def start_monitor(self):
        # type: () -> None
        self.__monitor_event = True

    def push_event(self, event):
        # type: (int) -> None
        if self.__monitor_event:
            self.__event.append(event)

    def stop_monitor(self):
        # type: () -> None
        self.__monitor_event = False
        self.__event.clear()
