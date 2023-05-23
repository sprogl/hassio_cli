class WrongInput(Exception):
    def __init__(self):
        super().__init__("wrong input format")


class DeviceNotExists(Exception):
    def __init__(self, name_device):
        super().__init__(f"{name_device} is not defined")


class ActionNotExists(Exception):
    def __init__(self, name_action):
        super().__init__(f"{name_action} is not defined for this device")


class InvalidType(Exception):
    def __init__(self, name_type):
        super().__init__(
            f"wrong config format: the device type {name_type} is not valid"
        )


class InvalidToken(Exception):
    def __init__(self):
        super().__init__("token is invalid")


class InvalidID(Exception):
    def __init__(self, id):
        super().__init__(f"wrong config format: the device ID {id} is not valid")


class HassioUnreachable(Exception):
    def __init__(self, url):
        super().__init__(f"Home Assistant is not reachable under {url}")


class InvalidURL(Exception):
    def __init__(self, url):
        super().__init__(f"wrong config format: invalid url format, {url}")


class URLTokenNotPresent(Exception):
    def __init__(self):
        super().__init__(
            "wrong config format: either url or token field is missing from the config file"
        )


class OffDevice(Exception):
    def __init__(self):
        super().__init__("the device is off")
