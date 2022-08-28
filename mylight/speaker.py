from mylight import const, protocol


DATA_VOLUME = 0
DATA_EQ = 1
DATA_EFFECT = 2


class Speaker():
    """
    Class for speaker part of bulb
    """

    _raw_data: list = []
    _mute: bool = False
    _volume: int = 0
    _equalizer: list = []
    _speaker_effect: str = None

    def __init__(self, send_func, update_func) -> None:
        self._send = send_func
        self._update = update_func
        self.update()

    def update(self):
        self._raw_data = self._update(
            const.SetBulbCategory.speaker,
            const.GetSpeakerFunction
        )
        self._mute = True if self._raw_data[DATA_VOLUME]['volume'] > 0 else False
        self._volume = self._raw_data[DATA_VOLUME]['volume']
        self._equalizer = self._raw_data[DATA_EQ]
        self._speaker_effect = None
        for speaker_effect in const.SpeakerEffectEqualizer:
            if speaker_effect.value == self._equalizer:
                self._speaker_effect = speaker_effect.name

    def send(self, msg):
        self._send(msg)
        self.update()

    def set_speaker_level(self, level, function='volume'):
        """
        Set speaker levels for volume and equalizer

        :param level: The level for the speaker function. Between 0 and 100
        :param speaker_function: An speaker function\
        ;(see :class:`.SetSpeakerFunction`)
        """
        max_level = 0x4f  # 79
        level_modified = int(level * max_level / 100)
        return self.send(protocol.encode_msg(
            const.SetBulbCategory.speaker.value,
            const.SetSpeakerFunction[function].value,
            level_modified)
        )

    def set_speaker_effect(self, effect):
        """
        Set speaker effect, flat, classical, pop, bass, jazz

        :param speaker_effect: An speaker effect (see :class:`.SpeakerEffect`)
        """
        return self.send(protocol.encode_msg(
            const.SetBulbCategory.speaker.value,
            const.SetSpeakerFunction.speaker_effect.value,
            const.SpeakerEffect[effect].value)
        )

    @property
    def mute(self):
        """Get mute."""
        return self._mute

    @property
    def volume(self):
        """Get volume."""
        return self._volume

    @property
    def effect(self):
        """Get effect """
        return self._speaker_effect

    @property
    def equalizer(self):
        """Get equalizer """
        return self._equalizer
