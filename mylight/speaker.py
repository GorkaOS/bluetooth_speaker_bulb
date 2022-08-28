from mylight import const, protocol


DATA_VOLUME = 0
DATA_EQ = 1
DATA_EFFECT = 2


class Speaker():
    """
    class for speaker part of bulb
    """

    _data = []

    def __init__(self, send_func, update_func) -> None:
        self._send = send_func
        self._update = update_func
        self.update()

    def update(self):
        self._data = self._update(
            const.SetBulbCategory.speaker,
            const.GetSpeakerFunction
        )

    def set_speaker_level(self, level, function):
        """
        Set speaker levels for volume and equalizer

        :param level: The level for the speaker function. Between 0 and 100
        :param speaker_function: An speaker function\
        ;(see :class:`.SetSpeakerFunction`)
        """
        max_level = 0x4f  # 79
        level_modified = int(level * max_level / 100)
        return self._send(protocol.encode_msg(
            const.SetBulbCategory.speaker.value,
            const.SetSpeakerFunction[function].value,
            level_modified)
        )

    def set_speaker_effect(self, effect):
        """
        Set speaker effect, flat, classical, pop, bass, jazz

        :param speaker_effect: An speaker effect (see :class:`.SpeakerEffect`)
        """
        self.effect = effect
        return self._send(protocol.encode_msg(
            const.SetBulbCategory.speaker.value,
            const.SetSpeakerFunction.speaker_effect.value,
            const.SpeakerEffect[effect].value)
        )

    @property
    def volume(self):
        """Get volume."""
        return self._data[DATA_VOLUME]['volume']

    @property
    def effect(self):
        """Get effect """
        try:
            return self._data[DATA_EFFECT]['effect']
        except IndexError:
            return None

    @effect.setter
    def effect(self, value):
        """Set effect """
        self._data.append({'effect': value})

    def eq(self):
        """Get eq """
        return self._data[DATA_EQ]
