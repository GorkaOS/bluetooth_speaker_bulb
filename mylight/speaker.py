from mylight import const, protocol


DATA_VOLUME = 0
DATA_EQ = 1


class Speaker():
    """
    Class for speaker part of bulb
    """

    def __init__(self) -> None:
        self._raw_data: list = None
        self._mute: bool = None
        self._volume: int = None
        self._equalizer: list = None
        self._speaker_effect: str = None

    def update(self, raw_data: list):
        print(raw_data[DATA_VOLUME]['volume'])
        self._mute = False if raw_data[DATA_VOLUME]['volume'] > 0 else True

        min_level = const.SpeakerEqualizerLevelMin.volume.value
        max_level = const.SpeakerEqualizerLevelMax.volume.value
        steps = len(range(min_level, max_level))
        self._volume = \
            int(raw_data[DATA_VOLUME]['volume'] * 100 / steps)

        self._equalizer = raw_data[DATA_EQ]
        self._speaker_effect = None
        for speaker_effect in const.SpeakerEffectEqualizer:
            if speaker_effect.value == self._equalizer:
                self._speaker_effect = speaker_effect.name

    def set_speaker_level(self, level, function=const.SetSpeakerFunction.volume.name):
        """
        Set speaker levels for volume and equalizer

        :param level: The level for the speaker function. Between 0 and 100
        :param speaker_function: An speaker function\
        ;(see :class:`.SetSpeakerFunction`)
        """
        min_level = const.SpeakerEqualizerLevelMin[function].value
        max_level = const.SpeakerEqualizerLevelMax[function].value

        steps = len(range(min_level, max_level))
        level_modified = int(level / 100 * steps)

        return protocol.encode_msg(
            const.SetBulbCategory.speaker.value,
            const.SetSpeakerFunction[function].value,
            level_modified
        )

    def set_speaker_effect(self, effect):
        """
        Set speaker effect, flat, classical, pop, bass, jazz

        :param speaker_effect: An speaker effect (see :class:`.SpeakerEffect`)
        """
        self._effect = effect
        return protocol.encode_msg(
            const.SetBulbCategory.speaker.value,
            const.SetSpeakerFunction.speaker_effect.value,
            const.SpeakerEffect[effect].value
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
