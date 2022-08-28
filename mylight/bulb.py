from mylight.connection import Connection
from mylight.light import Light
from mylight.speaker import Speaker


class Bulb():

    def __init__(self, mac_address, adapter, retries) -> None:
        self._connection = Connection(mac_address, adapter, retries)
        self._light = Light(func=self._connection.send_message)
        self._speaker = Speaker(func=self._connection.send_message)
        pass

    def connect(self):
        self._connection.connect()

    def disconnect(self):
        self._connection.disconnect()

    def get_device_name(self):
        return self._connection.get_device_name()

    def turn_on(self, brightness=None, rgb_color=None):
        self._light.on = True

    def turn_off(self):
        # return self._connection.send_message(self._light.turn_off())
        self._light.on = False

    def set_brightness(self, brightness):
        # return self._connection.send_message(self._light.set_brightness(brightness))
        if self._light.brightness == brightness or self._light.white:
            self.turn_on()
        elif brightness == 0:
            self.turn_off()
        self._light.brightness = brightness

    def set_rgb_color(self, rgb_color):
        # return self._connection.send_message(self._light.set_rgb_color(rgb_color))
        self._light.rgb_color = rgb_color

    def set_white(self):
        # return self._connection.send_message(self._light.set_white())
        self._light.white = True

    def set_effect(self, effect):
        self._light.effect = effect
        # return self._connection.send_message(self._light.set_effect(effect))

    def set_volume(self, volume):
        self._speaker.volume = volume

    def set_speaker_effect(self, effect):
        self._speaker.effect = effect
