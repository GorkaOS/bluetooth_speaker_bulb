import logging

from .const import *
from .protocol import *

_LOGGER = logging.getLogger(__name__)

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
        if not raw_data:
            _LOGGER.debug(f"Updating speaker failed, raw_data: {raw_data}")
            return
        _LOGGER.debug(f"Updating speaker, raw_data: {raw_data}")
        self._mute = False if raw_data[DATA_VOLUME]['volume'] > 0 else True

        min_level = SpeakerEqualizerLevelMin.volume.value
        max_level = SpeakerEqualizerLevelMax.volume.value
        steps = len(range(min_level, max_level))
        self._volume = \
            int(raw_data[DATA_VOLUME]['volume'] * 100 / steps)

        self._equalizer = raw_data[DATA_EQ]
        self._speaker_effect = None
        for speaker_effect in SpeakerEffectEqualizer:
            if speaker_effect.value == self._equalizer:
                self._speaker_effect = speaker_effect.name

    def set_speaker_level(self, level, function=SetSpeakerFunction.volume.name):
        """
        Set speaker levels for volume and equalizer

        :param level: The level for the speaker function. Between 0 and 100
        :param speaker_function: An speaker function\
        ;(see :class:`.SetSpeakerFunction`)
        """
        min_level = SpeakerEqualizerLevelMin[function].value
        max_level = SpeakerEqualizerLevelMax[function].value

        steps = len(range(min_level, max_level))
        level_modified = int(level / 100 * steps)

        return encode_msg(
            SetBulbCategory.speaker.value,
            SetSpeakerFunction[function].value,
            level_modified
        )

    def set_speaker_effect(self, effect):
        """
        Set speaker effect, flat, classical, pop, bass, jazz

        :param speaker_effect: An speaker effect (see :class:`.SpeakerEffect`)
        """
        self._effect = effect
        return encode_msg(
            SetBulbCategory.speaker.value,
            SetSpeakerFunction.speaker_effect.value,
            SpeakerEffect[effect].value
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
