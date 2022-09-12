from mylight import const, protocol

DATA_LIGHT = 0


class Light():
    """
    Class for speaker part of bulb
    """

    def __init__(self) -> None:
        self._on: bool = None
        self._brightness: int = None
        self._cold: int = None
        self._warm: int = None
        self._temperature: int = self._cold
        self._rgb: list = None
        self._white: bool = True
        self._effect_id: int = None
        self._effect: str = None

    def update(self, raw_data: list):
        self._on = raw_data[DATA_LIGHT]['on']
        self._brightness = raw_data[DATA_LIGHT]['brightness']
        self._cold = raw_data[DATA_LIGHT]['cold']
        self._warm = raw_data[DATA_LIGHT]['warm']
        self._temperature = self._cold
        self._rgb = [
            raw_data[DATA_LIGHT]['r'],
            raw_data[DATA_LIGHT]['g'],
            raw_data[DATA_LIGHT]['b']
        ]
        self._white = True if self._warm > 0 or self._cold > 0 else False
        self._effect_id = raw_data[DATA_LIGHT]['effect_raw']
        if (self._effect_id > 0):
            try:
                self._effect_id -= 1
                self._effect = const.Effects(self._effect_id).name
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

    def set_color_rgb(self, rgb):
        """
        Change bulb's color

        :param rgb_color: color as a list of 3 values between 0 and 255
        """
        self._rgb = rgb
        self._white = False
        return protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.color.value,
            rgb
        )

    def set_white(self):
        """
        Set white

        """
        self._white = True
        self._rgb = None
        return protocol.encode_msg(
            const.SetBulbCategory.light.value,
            const.SetLightFunction.white.value,
            const.Commands.ON.value
        )

    def set_white_intensity(self, intensity: int):
        """
        Set white intensity
        ;param intensity: value between 1..255
        """
        return protocol.encode_msg(
            const.SetBulbCategory.lamp.value,
            const.SetLightFunction.white_intensity.value,
            intensity
        )

    def set_effect(self, effect):
        """
        Set an effect

        :param effect: An effect
        """
        self._effect = effect
        c = const.Effects[effect].value[0]
        e = const.Effects[effect].value[1]
        if c == const.SetLightFunction.white:
            self._white = True
        else:
            self._white = False
        return protocol.encode_msg(
            const.SetBulbCategory.light.value,
            c,
            e
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
        return self._rgb

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

    @property
    def temperature(self) -> int:
        """Return if temperature is on or off"""
        return self._temperature
