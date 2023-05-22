class WrongInput(Exception):
    def __init__(self):
        super().__init__("wrong input format")


class NoInput(Exception):
    def __init__(self):
        super().__init__("both arguments --device and --action must be supplied")


class OffDevice(Exception):
    def __init__(self):
        super().__init__("the device is off")
