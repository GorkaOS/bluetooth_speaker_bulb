from mylight import const, protocol

class Light():
    """
    """

    def __init__(self,
                 func,
                 on=False,
                 brightness=0,
                 rgb_color=[0, 0, 0],
                 white=True,
                 effect=None,
                 white_effect=None
                 ) -> None:
        self._func = func
        self._on = on
        self._brightness = brightness
        self._rgb_color = rgb_color
        self._white = white
        self._effect = effect
        self._white_effect = white_effect

    def turn_off(self) -> str:
        """
        Turn off the light
        """
        msg = protocol.encode_msg(const.SetBulbCategory.light.value,
                                  const.SetLightFunction.power.value,
                                  const.Commands.OFF.value)
        msg.append(protocol.encode_checksum(msg))
        self._func(msg)

    def turn_on(self) -> list:
        """
        Set white color on the light

        :param brightness: a float value between 0.0 and 1.0 defining the
            brightness
        """
        # if brightness == self._brightness or brightness is None:
        msg = protocol.encode_msg(const.SetBulbCategory.light.value,
                                    const.SetLightFunction.power.value,
                                    const.Commands.ON.value)
        msg.append(protocol.encode_checksum(msg))
        self._func(msg)



    def set_brightness(self, brightness) -> str:
        """
        Set Brightness

        :param intensity: brightness between 0..255
        """
        msg = protocol.encode_msg(const.SetBulbCategory.light.value,
                                  const.SetLightFunction.brightness.value,
                                  brightness)
        msg.append(protocol.encode_checksum(msg))
        self._func(msg)
        
    def set_rgb_color(self, rgb_color):
        """
        Change bulb's color

        :param rgb_color: color as a list of 3 values between 0 and 255
        """
        msg = protocol.encode_msg(const.SetBulbCategory.light.value,
                                  const.SetLightFunction.color.value,
                                  rgb_color)
        msg.append(protocol.encode_checksum(msg))
        self._func(msg)

    def set_white(self):
        """
        Set white

        """
        msg = protocol.encode_msg(const.SetBulbCategory.light.value,
                                  const.SetLightFunction.white_effect.value,
                                  const.Commands.ON.value)
        msg.append(protocol.encode_checksum(msg))
        self._func(msg)

    def set_effect(self, effect):
        """
        Set an effect

        :param effect: An effect
        """
        msg = protocol.encode_msg(const.SetBulbCategory.light.value,
                                  const.SetLightFunction.effect.value,
                                  const.LightEffect[effect].value)
        msg.append(protocol.encode_checksum(msg))
        self._func(msg)

    @property
    def on(self) -> bool:
        """Get on."""
        return self._on

    @on.setter
    def on(self, value):
        """Set on."""
        self._on = value
        if self._on:
            self.turn_on()
        else:
            self.turn_off()

    @property
    def brightness(self) -> int:
        """Get brightness level."""
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        """Set brightness level."""
        self._brightness = value
        self.set_brightness(self._brightness)

    @property
    def rgb_color(self):
        """Get color."""
        return self._rgb_color

    @rgb_color.setter
    def rgb_color(self, value):
        """Set color as list of [R, G, B], each 0-255."""
        self._rgb_color = value
        self._white = False
        self.set_rgb_color(self._rgb_color)

    @property
    def white(self):
        """Get white."""
        return self._white

    @white.setter
    def white(self, value):
        """Set white"""
        self._white = value
        self._rgb_color = None
        self.set_white(self._white)

    @property
    def effect(self):
        """Get effect """
        return self._effect

    @effect.setter
    def effect(self, value):
        """Set effect """
        self._effect = value
        self.set_effect(self._effect)
