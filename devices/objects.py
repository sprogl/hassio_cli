import re
import exceptions.exceptions as exceptions
import devices.api

valid_types = ["dimmable-lamp", "plug", "home", "player", "tv"]


def parse_object(
    object_type: str, id: str, api_iface: devices.api.API_interface
) -> object:
    if object_type == "dimmable-lamp":
        return Dimmable_lamp(id=id, api_iface=api_iface)
    elif object_type == "plug":
        return Plug(id=id, api_iface=api_iface)
    elif object_type == "home":
        return Home(id=id, api_iface=api_iface)
    elif object_type == "player":
        return Player(id=id, api_iface=api_iface)
    elif object_type == "tv":
        return TV(id=id, api_iface=api_iface)
    else:
        raise exceptions.WrongInput


class Dimmable_lamp(object):
    def __init__(self, id: str, api_iface: devices.api.API_interface):
        self._id = id
        self._api_iface = api_iface

    def __getitem__(self, key) -> str:
        if isinstance(key, str):
            return self.parse_action(key)
        else:
            raise KeyError

    def __str__(self) -> str:
        return f'dimmable lamp with the id "{self._id}"'

    def turn_on(self) -> str:
        endpoint = "/api/services/light/turn_on"
        data = {"entity_id": self._id}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def turn_off(self) -> str:
        endpoint = "/api/services/light/turn_off"
        data = {"entity_id": self._id}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def set_brightness(self, percentage: int) -> str:
        if percentage < 0 or percentage > 100:
            raise exceptions.WrongInput
        endpoint = "/api/services/light/turn_on"
        data = {"entity_id": self._id, "brightness": round(2.55 * percentage)}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def parse_action(self, action_str: str) -> str:
        if action_str == "on":
            return self.turn_on()
        elif action_str == "off":
            return self.turn_off()
        elif re.compile("set-br-[0-9]+").fullmatch(action_str):
            percentage = int(action_str[7:])
            return self.set_brightness(percentage)
        else:
            raise exceptions.WrongInput


class Plug(object):
    def __init__(self, id: str, api_iface: devices.api.API_interface):
        self._id = id
        self._api_iface = api_iface

    def __getitem__(self, key) -> str:
        if isinstance(key, str):
            return self.parse_action(key)
        else:
            raise KeyError

    def __str__(self) -> str:
        return f'smart plug with the id "{self._id}"'

    def turn_on(self) -> str:
        endpoint = "/api/services/switch/turn_on"
        data = {"entity_id": self._id}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def turn_off(self) -> str:
        endpoint = "/api/services/switch/turn_off"
        data = {"entity_id": self._id}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def parse_action(self, action_str: str) -> str:
        if action_str == "on":
            return self.turn_on()
        elif action_str == "off":
            return self.turn_off()
        else:
            raise exceptions.WrongInput


class Home(object):
    def __init__(self, id: str, api_iface: devices.api.API_interface):
        self._id = id
        self._api_iface = api_iface

    def __getitem__(self, key) -> str:
        if isinstance(key, str):
            return self.parse_action(key)
        else:
            raise KeyError

    def __str__(self) -> str:
        return f'home with the id "{self._id}"'

    def turn_on(self) -> str:
        endpoint = "/api/services/input_boolean/turn_on"
        data = {"entity_id": self._id}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def turn_off(self) -> str:
        endpoint = "/api/services/input_boolean/turn_off"
        data = {"entity_id": self._id}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def parse_action(self, action_str: str) -> str:
        if action_str == "on":
            return self.turn_on()
        elif action_str == "off":
            return self.turn_off()
        else:
            raise exceptions.WrongInput


class Player(object):
    def __init__(self, id: str, api_iface: devices.api.API_interface):
        self._id = id
        self._api_iface = api_iface

    def __getitem__(self, key) -> str:
        if isinstance(key, str):
            return self.parse_action(key)
        else:
            raise KeyError

    def __str__(self) -> str:
        return f'tv with the id "{self._id}"'

    def turn_on(self) -> str:
        endpoint = "/api/services/media_player/turn_on"
        data = {"entity_id": self._id}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def turn_off(self) -> str:
        endpoint = "/api/services/media_player/turn_off"
        data = {"entity_id": self._id}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def play(self) -> str:
        endpoint = "/api/services/media_player/media_play"
        data = {"entity_id": self._id}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def pause(self) -> str:
        endpoint = "/api/services/media_player/media_pause"
        data = {"entity_id": self._id}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def stop(self) -> str:
        endpoint = "/api/services/media_player/media_stop"
        data = {"entity_id": self._id}
        return self._api_iface.post(endpoint=endpoint, data=data)

    # def mute(self) -> str:
    #     endpoint = "/api/services/media_player/volume_mute"
    #     data = {"entity_id": self._id, "is_volume_muted": False}
    #     return self._api_iface.post(endpoint=endpoint, data=data)

    def set_volume(self, percentage: int) -> str:
        if percentage < 0 or percentage > 100:
            raise exceptions.WrongInput
        endpoint = "/api/services/media_player/volume_set"
        data = {"entity_id": self._id, "volume_level": 1e-2 * percentage}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def parse_action(self, action_str: str) -> str:
        if action_str == "on":
            return self.turn_on()
        elif action_str == "off":
            return self.turn_off()
        elif action_str == "play":
            return self.play()
        elif action_str == "pause":
            return self.pause()
        elif action_str == "stop":
            return self.stop()
        # elif action_str == "mute":
        #     return self.mute()
        elif re.compile("set-vol-[0-9]+").fullmatch(action_str):
            percentage = int(action_str[8:])
            return self.set_volume(percentage)
        else:
            raise exceptions.WrongInput


class TV(Player):
    _channel_chrome_cast = "cast"
    _channel_erste = "erste"
    _channel_zdf = "zdf"
    _channel_youtube = "yt"

    def set_channel(self, channel: str) -> str:
        endpoint = "/api/services/media_player/select_source"
        match channel:
            case self._channel_chrome_cast:
                data = {"entity_id": self._id, "source": "HDMI"}
            case self._channel_erste:
                data = {"entity_id": self._id, "source": "ARD Mediathek"}
            case self._channel_zdf:
                data = {"entity_id": self._id, "source": "ZDF mediathek"}
            case self._channel_youtube:
                data = {"entity_id": self._id, "source": "YouTube"}
            case _:
                raise exceptions.WrongInput
        return self._api_iface.post(endpoint=endpoint, data=data)

    def parse_action(self, action_str: str) -> str:
        if action_str == "on":
            return self.turn_on()
        elif action_str == "off":
            return self.turn_off()
        elif action_str == "play":
            return self.play()
        elif action_str == "pause":
            return self.pause()
        elif action_str == "stop":
            return self.stop()
        # elif action_str == "mute":
        #     return self.mute()
        elif re.compile("set-vol-[0-9]+").fullmatch(action_str):
            percentage = int(action_str[8:])
            return self.set_volume(percentage)
        elif re.compile("set-ch-[a-z]+").fullmatch(action_str):
            channel = action_str[7:]
            return self.set_channel(channel)
        else:
            raise exceptions.WrongInput
