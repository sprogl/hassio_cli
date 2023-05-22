import re
import exceptions.exceptions as exceptions
import devices.api
import json
import requests.exceptions

valid_types = ["dimmable-lamp", "plug", "home", "player", "tv"]


def parse_object(
    object_type: str, id: str, api_iface: devices.api.API_interface
) -> object:
    if object_type == "dimmable-lamp":
        return DimmableLamp(id=id, api_iface=api_iface)
    elif object_type == "plug":
        return Plug(id=id, api_iface=api_iface)
    elif object_type == "home":
        return Home(id=id, api_iface=api_iface)
    elif object_type == "player":
        return Player(id=id, api_iface=api_iface)
    elif object_type == "tv":
        return TV(id=id, api_iface=api_iface)
    else:
        raise exceptions.InvalidType(object_type)


class Hassiodevice(object):
    def __init__(self, id: str, api_iface: devices.api.API_interface):
        self._id = id
        self._api_iface = api_iface
        # self._update()
        try:
            self._update()
        except requests.exceptions.ConnectionError:
            raise exceptions.HassioUnreachable(api_iface["url"])
        if str(self._data) == "{'message': 'Entity not found.'}":
            raise exceptions.InvalidID(id)

    def __getitem__(self, key) -> str:
        try:
            if isinstance(key, str):
                return self._parse_action(key)
            else:
                raise KeyError
        except exceptions.OffDevice:
            return "the device is off"
        except exceptions.WrongInput:
            return "wrong iput format"

    def _update(self):
        endpoint = f"/api/states/{self._id}"
        response = self._api_iface.get(endpoint=endpoint)
        data = json.loads(response)
        self._data = data

    def get_state(self) -> str:
        self._update()
        return self._data["state"]

    def _is_on(self) -> bool:
        return self._data["state"] != "off"


class DimmableLamp(Hassiodevice):
    def __str__(self) -> str:
        return f'dimmable lamp with the id "{self._id}"'

    def turn_on(self) -> str:
        endpoint = "/api/services/light/turn_on"
        data = {"entity_id": self._id}
        self._update()
        if not self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            return "it is already on"

    def turn_off(self) -> str:
        endpoint = "/api/services/light/turn_off"
        data = {"entity_id": self._id}
        self._update()
        if self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            return "it is already off"

    def set_brightness(self, percentage: int) -> str:
        if percentage < 0 or percentage > 100:
            raise exceptions.WrongInput
        endpoint = "/api/services/light/turn_on"
        data = {"entity_id": self._id, "brightness": round(2.55 * percentage)}
        return self._api_iface.post(endpoint=endpoint, data=data)

    def parse_action(self, action_str: str) -> str:
        if action_str == "is-on":
            self._update()
            if self._is_on():
                return "yes"
            else:
                return "no"
        elif action_str == "get-state":
            return self.get_state()
        elif action_str == "on":
            return self.turn_on()
        elif action_str == "off":
            return self.turn_off()
        elif re.compile("set-br-[0-9]+").fullmatch(action_str):
            percentage = int(action_str[7:])
            return self.set_brightness(percentage)
        else:
            raise exceptions.ActionNotExists(action_str)


class Plug(Hassiodevice):
    def __str__(self) -> str:
        return f'smart plug with the id "{self._id}"'

    def turn_on(self) -> str:
        endpoint = "/api/services/switch/turn_on"
        data = {"entity_id": self._id}
        self._update()
        if not self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            return "it is already on"

    def turn_off(self) -> str:
        endpoint = "/api/services/switch/turn_off"
        data = {"entity_id": self._id}
        self._update()
        if self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            return "it is already off"

    def parse_action(self, action_str: str) -> str:
        if action_str == "is-on":
            self._update()
            if self._is_on():
                return "yes"
            else:
                return "no"
        elif action_str == "get-state":
            return self.get_state()
        elif action_str == "on":
            return self.turn_on()
        elif action_str == "off":
            return self.turn_off()
        else:
            raise exceptions.ActionNotExists(action_str)


class Home(Hassiodevice):
    def __str__(self) -> str:
        return f'home with the id "{self._id}"'

    def occupy(self) -> str:
        endpoint = "/api/services/input_boolean/turn_on"
        data = {"entity_id": self._id}
        self._update()
        if not self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            return "home is already occupied"

    def leave(self) -> str:
        endpoint = "/api/services/input_boolean/turn_off"
        data = {"entity_id": self._id}
        self._update()
        if self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            return "home is already left"

    def parse_action(self, action_str: str) -> str:
        if action_str == "is-on":
            self._update()
            if self._is_on():
                return "yes"
            else:
                return "no"
        elif action_str == "get-state":
            return self.get_state()
        elif action_str == "on":
            return self.occupy()
        elif action_str == "off":
            return self.leave()
        else:
            raise exceptions.ActionNotExists(action_str)


class Player(Hassiodevice):
    def __getitem__(self, key) -> str:
        try:
            if isinstance(key, str):
                return self._parse_action(key)
            else:
                raise KeyError
        except exceptions.OffDevice:
            return "the device is off"
        except exceptions.WrongInput:
            return "wrong iput format"

    def __str__(self) -> str:
        return f'madia player with the id "{self._id}"'

    def _update(self):
        endpoint = f"/api/states/{self._id}"
        response = self._api_iface.get(endpoint=endpoint)
        data = json.loads(response)
        self._data = data

    def turn_on(self) -> str:
        endpoint = "/api/services/media_player/turn_on"
        data = {"entity_id": self._id}
        self._update()
        if not self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            return "it is already on"

    def turn_off(self) -> str:
        endpoint = "/api/services/media_player/turn_off"
        data = {"entity_id": self._id}
        self._update()
        if self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            return "it is already off"

    def play(self) -> str:
        endpoint = "/api/services/media_player/media_play"
        data = {"entity_id": self._id}
        self._update()
        if self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)

    def pause(self) -> str:
        endpoint = "/api/services/media_player/media_pause"
        data = {"entity_id": self._id}
        self._update()
        if self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            raise exceptions.OffDevice

    def stop(self) -> str:
        endpoint = "/api/services/media_player/media_stop"
        data = {"entity_id": self._id}
        self._update()
        if self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            raise exceptions.OffDevice

    def is_mute(self) -> bool:
        self._update()
        if self._is_on():
            return self._data["is_volume_muted"]
        else:
            raise exceptions.OffDevice

    def mute(self) -> str:
        endpoint = "/api/services/media_player/volume_mute"
        self._update()
        if self._is_on():
            data = {
                "entity_id": self._id,
                "is_volume_muted": self._data["is_volume_muted"],
            }
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            raise exceptions.OffDevice

    def get_volume(self) -> str:
        self._update()
        if self._is_on():
            return str(round(1e2 * self._data["attributes"]["volume_level"]))
        else:
            raise exceptions.OffDevice

    def set_volume(self, percentage: int) -> str:
        if percentage < 0 or percentage > 100:
            raise exceptions.WrongInput
        endpoint = "/api/services/media_player/volume_set"
        data = {"entity_id": self._id, "volume_level": 1e-2 * percentage}
        self._update()
        if self._is_on():
            return self._api_iface.post(endpoint=endpoint, data=data)
        else:
            raise exceptions.OffDevice

    def _parse_action(self, action_str: str) -> str:
        if action_str == "is-on":
            self._update()
            if self._is_on():
                return "yes"
            else:
                return "no"
        elif action_str == "get-state":
            return self.get_state()
        elif action_str == "on":
            return self.turn_on()
        elif action_str == "off":
            return self.turn_off()
        elif action_str == "play":
            return self.play()
        elif action_str == "pause":
            return self.pause()
        elif action_str == "stop":
            return self.stop()
        elif action_str == "is-mute":
            if self.is_mute():
                return "yes"
            else:
                return "no"
        elif action_str == "mute":
            return self.mute()
        elif action_str == "get-vol":
            return self.get_volume()
        elif re.compile("set-vol-[0-9]+").fullmatch(action_str):
            percentage = int(action_str[8:])
            return self.set_volume(percentage)
        else:
            raise exceptions.ActionNotExists(action_str)


class TV(Player):
    _channels_dict = {
        "cast": "HDMI",
        "erste": "ARD Mediathek",
        "zdf": "ZDF mediathek",
        "yt": "YouTube",
    }

    def set_channel(self, channel: str) -> str:
        endpoint = "/api/services/media_player/select_source"
        try:
            data = {"entity_id": self._id, "source": self._channels_dict[channel]}
        except KeyError:
            raise exceptions.WrongInput
        return self._api_iface.post(endpoint=endpoint, data=data)

    def parse_action(self, action_str: str) -> str:
        if action_str == "is-on":
            self._update()
            if self._is_on():
                return "yes"
            else:
                return "no"
        elif action_str == "get-state":
            return self.get_state()
        elif action_str == "on":
            return self.turn_on()
        elif action_str == "off":
            return self.turn_off()
        elif action_str == "play":
            return self.play()
        elif action_str == "pause":
            return self.pause()
        elif action_str == "stop":
            return self.stop()
        elif action_str == "is-mute":
            if self.is_mute():
                return "yes"
            else:
                return "no"
        elif action_str == "mute":
            return self.mute()
        elif action_str == "get-vol":
            return self.get_volume()
        elif re.compile("set-vol-[0-9]+").fullmatch(action_str):
            percentage = int(action_str[8:])
            return self.set_volume(percentage)
        elif re.compile("set-ch-[a-z]+").fullmatch(action_str):
            channel = action_str[7:]
            return self.set_channel(channel)
        else:
            raise exceptions.ActionNotExists(action_str)
