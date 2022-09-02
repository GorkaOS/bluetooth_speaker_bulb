from mylight import const, protocol

DATA_LIGHT = 0


class Light():
    """
    Class for speaker part of bulb
    """
    _on: bool
    _brightness: int
    _cold: int
    _warm: int
    _rgb_color: list
    _white: bool
    _effect_id: int
    _effect: str

    def __init__(self, raw_data: list) -> None:
        self.update(raw_data=raw_data)

    def update(self, raw_data: list):
        self._on = raw_data[DATA_LIGHT]['on']
        self._brightness = raw_data[DATA_LIGHT]['brightness']
        self._cold = raw_data[DATA_LIGHT]['cold']
        self._warm = raw_data[DATA_LIGHT]['warm']
        self._rgb_color = [
            raw_data[DATA_LIGHT]['r'],
            raw_data[DATA_LIGHT]['g'],
            raw_data[DATA_LIGHT]['b']
        ]
        self._white = True if self._warm > 0 or self._cold > 0 else False
        self._effect_id = raw_data[DATA_LIGHT]['effect_raw']
        if (self._effect_id > 0):
            try:
                self._effect_id -= 1
                self._effect = const.LightEffect(self._effect_id).name
            except ValueError:
                pass
        else:
            self._effect = None

    def turn_off(self) -> str:
        """
        Turn off the light
        """
        self._on = False
        return protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.power.value,
            const.Commands.OFF.value
        )

    def turn_on(self) -> str:
        """
        Set white color on the light

        :param brightness: a float value between 0.0 and 1.0 defining the
            brightness
        """
        self._on = True
        return protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.power.value,
            const.Commands.ON.value
        )

    def set_brightness(self, brightness) -> str:
        """
        Set Brightness

        :param intensity: brightness between 0..255
        """
        self._brightness = brightness
        return protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.brightness.value,
            brightness
        )

    def set_rgb_color(self, rgb_color):
        """
        Change bulb's color

        :param rgb_color: color as a list of 3 values between 0 and 255
        """
        self._rgb_color = rgb_color
        return protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.color.value,
            rgb_color
        )

    def set_white(self):
        """
        Set white

        """
        self._white = True
        return protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.white_effect.value,
            const.Commands.ON.value
        )

    def set_effect(self, effect):
        """
        Set an effect

        :param effect: An effect
        """
        self._effect = effect
        return protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.effect.value,
            const.LightEffect[effect].value
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
