from mylight.connection import Connection
from mylight.light import Light
from mylight.speaker import Speaker


class Bulb():

    def __init__(self, mac_address, adapter, retries) -> None:
        self._connection = Connection(mac_address, adapter, retries)
        self._light = Light(
            send_func=self._connection.send_message,
            update_func=self._connection.get_category_info
        )
        self._speaker = Speaker(
            send_func=self._connection.send_message,
            update_func=self._connection.get_category_info
        )
        pass

    def connect(self) -> bool:
        return self._connection.connect()

    def disconnect(self) -> bool:
        return self._connection.disconnect()

    def get_device_name(self) -> str:
        return self._connection.get_device_name()

    def get_light_info(self) -> str:
        return self._light.update()

    def get_speaker_info(self) -> str:
        return self._speaker.update()

    def turn_on(self, brightness=None, rgb_color=None) -> bool:
        return self._light.turn_on()

    def turn_off(self) -> bool:
        return self._light.turn_off()

    def set_brightness(self, brightness) -> bool:
        if self._light.brightness == brightness:
            self.turn_on()
        elif brightness == 0:
            self.turn_off()
        return self._light.set_brightness(brightness=brightness)

    def set_rgb_color(self, rgb_color) -> bool:
        return self._light.set_rgb_color(rgb_color=rgb_color)

    def set_white(self) -> bool:
        return self._light.set_white()

    def set_effect(self, effect) -> bool:
        return self._light.set_effect(effect=effect)

    def set_volume(self, volume) -> bool:
        return self._speaker.set_speaker_level(volume=volume)

    def set_speaker_effect(self, effect) -> bool:
        return self._speaker.set_speaker_effect(effect=effect)
