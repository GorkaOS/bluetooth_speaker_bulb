from mylight import const, protocol

DATA_LIGHT = 0


class Light():
    """
    Class for speaker part of bulb
    """

    _raw_data: list = []
    _on: bool = False
    _brightness: int = 0
    _cold: int = 0
    _warm: int = 0
    _rgb_color: list = [0, 0, 0]
    _white: bool = False
    _effect_id: int = 0
    _effect: str = None

    def __init__(self, send_func, update_func) -> None:
        self._send = send_func
        self._update = update_func
        self.update()

    def update(self):
        self._raw_data = self._update(
            const.SetBulbCategory.light,
            const.GetLightFunction
        )
        self._on = self._raw_data[DATA_LIGHT]['on']
        self._brightness = self._raw_data[DATA_LIGHT]['brightness']
        self._cold = self._raw_data[DATA_LIGHT]['cold']
        self._warm = self._raw_data[DATA_LIGHT]['warm']
        self._rgb_color = [
            self._raw_data[DATA_LIGHT]['r'],
            self._raw_data[DATA_LIGHT]['g'],
            self._raw_data[DATA_LIGHT]['b']
        ]
        self._white = True if self._warm > 0 or self._cold > 0 else False
        self._effect_id = self._raw_data[DATA_LIGHT]['effect_raw']
        if (self._effect_id > 0):
            try:
                self._effect_id -= 1
                self._effect = const.LightEffect(self._effect_id).name
            except ValueError:
                pass
        else:
            self._effect = None

    def send(self, msg):
        self._send(msg)
        self.update()

    def turn_off(self) -> bool:
        """
        Turn off the light
        """
        return self.send(protocol.encode_msg(
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
        return self.send(protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.power.value,
            const.Commands.ON.value)
        )

    def set_brightness(self, brightness) -> str:
        """
        Set Brightness

        :param intensity: brightness between 0..255
        """
        return self.send(protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.brightness.value,
            brightness)
        )

    def set_rgb_color(self, rgb_color):
        """
        Change bulb's color

        :param rgb_color: color as a list of 3 values between 0 and 255
        """
        return self.send(protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.color.value,
            rgb_color)
        )

    def set_white(self):
        """
        Set white

        """
        self.white = True
        return self.send(protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.white_effect.value,
            const.Commands.ON.value)
        )

    def set_effect(self, effect):
        """
        Set an effect

        :param effect: An effect
        """
        return self.send(protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.effect.value,
            const.LightEffect[effect].value)
        )

    @property
    def on(self) -> bool:
        """Get on."""
        return self._on

    @property
    def brightness(self) -> int:
        """Get brightness level."""
        return self._brightness

    @property
    def rgb_color(self) -> list:
        """Get color."""
        return self._rgb_color

    @property
    def white(self) -> bool:
        """Get white."""
        return self._white

    @property
    def effect(self) -> str:
        """Get effect """
        return self._effect

    @property
    def effect_id(self) -> int:
        """Get effect """
        return self._effect_id
