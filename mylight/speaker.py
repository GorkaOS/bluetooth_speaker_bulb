from mylight import const, protocol


class Speaker():
    """
    class for speaker part of bulb
    """

    def __init__(self,
                 func,
                 mute=False,
                 volume=0,
                 eq=[],
                 effect=None
                 ) -> None:
        self._func = func
        self._mute = mute
        self._volume = volume
        self._eq = eq
        self._effect = effect

    def set_speaker_level(self, level, function):
        """
        Set speaker levels for volume and equalizer

        :param level: The level for the speaker function. Between 0 and 100
        :param speaker_function: An speaker function\
        ;(see :class:`.SetSpeakerFunction`)
        """
        max_level = 0x4f  # 79
        level_modified = int(level * max_level / 100)
        msg = protocol.encode_msg(const.SetBulbCategory.speaker.value,
                                  const.SetSpeakerFunction[function].value,
                                  level_modified)
        msg.append(protocol.encode_checksum(msg))
        return self._func(msg)

    def set_speaker_effect(self, effect):
        """
        Set speaker effect, flat, classical, pop, bass, jazz

        :param speaker_effect: An speaker effect (see :class:`.SpeakerEffect`)
        """
        msg = protocol.encode_msg(const.SetBulbCategory.speaker.value,
                                  const.SetSpeakerFunction.speaker_effect.value,
                                  const.SpeakerEffect[effect].value)
        msg.append(protocol.encode_checksum(msg))
        return self._func(msg)

    @property
    def volume(self):
        """Get volume."""
        return self._volume

    @volume.setter
    def volume(self, value):
        """Set volume"""
        self._volume = value

    @property
    def effect(self):
        """Get effect """
        return self._effect

    @effect.setter
    def effect(self, value):
        """Set effect """
        self._effect = value
