from mylight import const, protocol

DATA_LIGHT = 0


class Light():
    """
    """

    _data = []

    def __init__(self, send_func, update_func) -> None:
        self._send = send_func
        self._update = update_func
        self.update()

    def update(self):
        self._data = self._update(
            const.SetBulbCategory.light,
            const.GetLightFunction
        )

    def turn_off(self) -> bool:
        """
        Turn off the light
        """
        return self._send(protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.power.value,
            const.Commands.OFF.value)
        )

    def turn_on(self) -> bool:
        """
        Set white color on the light

        :param brightness: a float value between 0.0 and 1.0 defining the
            brightness
        """
        return self._send(protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.power.value,
            const.Commands.ON.value)
        )

    def set_brightness(self, brightness) -> str:
        """
        Set Brightness

        :param intensity: brightness between 0..255
        """
        return self._send(protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.brightness.value,
            brightness)
        )

    def set_rgb_color(self, rgb_color):
        """
        Change bulb's color

        :param rgb_color: color as a list of 3 values between 0 and 255
        """
        return self._send(protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.color.value,
            rgb_color)
        )

    def set_white(self):
        """
        Set white

        """
        self.white = True
        return self._send(protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.white_effect.value,
            const.Commands.ON.value)
        )

    def set_effect(self, effect):
        """
        Set an effect

        :param effect: An effect
        """
        return self._send(protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.effect.value,
            const.LightEffect[effect].value)
        )

    @property
    def on(self) -> bool:
        """Get on."""
        return self._data[DATA_LIGHT]['on']

    @on.setter
    def on(self, value):
        """Set on."""
        self._data[DATA_LIGHT]['on'] = value

    @property
    def brightness(self) -> int:
        """Get brightness level."""
        return self._data[DATA_LIGHT]['brightness']

    @property
    def rgb_color(self) -> list:
        """Get color."""
        return self._data[DATA_LIGHT]['rgb_color']

    @property
    def white(self) -> bool:
        """Get white."""
        return self._data[DATA_LIGHT]['white']

    @white.setter
    def white(self, value):
        """Set white"""
        self._data[DATA_LIGHT]['white'] = value

    @property
    def effect(self) -> str:
        """Get effect """
        return self._data[DATA_LIGHT]['effect']

    @property
    def effect_id(self) -> int:
        """Get effect """
        return self._data[DATA_LIGHT]['effect_id']
