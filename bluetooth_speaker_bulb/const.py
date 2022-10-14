from enum import Enum


class UUID_CHARACTERISTIC(Enum):
    """
    An enum of all UUID Characteristics
    """
    UUID_CHARACTERISTIC_RECV = "0000a041-0000-1000-8000-00805f9b34fb"
    UUID_CHARACTERISTIC_WRITE = "0000a040-0000-1000-8000-00805f9b34fb"
    UUID_CHARACTERISTIC_DEVICE_NAME = "00002a00-0000-1000-8000-00805f9b34fb"


class Commands(Enum):
    """
    An enum of commands
    """
    ON = 0x01
    OFF = 0x00
    REQ_DATA = 0x06


class SetBulbCategory(Enum):
    """
    An enum of all set catagories
    """
    speaker = 0x04
    timer = 0x05
    light = 0x08
    state = 0x0b


class GetBulbCategory(Enum):
    """
    An enum of all get catagories
    """
    speaker = 0x84
    timer = 0x85
    light = 0x88
    state = 0x8b


class SetLightFunction(Enum):
    """
    An enum of all set light functions
    """
    brightness = 0x01
    color = 0x02
    power = 0x05
    effect = 0x06
    white_intensity = 0x07
    white = 0x09


class GetLightFunction(Enum):
    """
    An enum of all get light functions
    """
    # ?? = 0x16
    status = 0x15


class LightEffect(Enum):
    """
    An enum of all the possible effects the bulb can accept
    """
    none = 0x00
    rainbow = 0x01                      #: bluetooth_speaker_bulb
    flowing = 0x02                      #: bluetooth_speaker_bulb
    heartbeat = 0x03                    #: bluetooth_speaker_bulb
    red_pulse = 0x04                    #: bluetooth_speaker_bulb
    green_pulse = 0x05                  #: bluetooth_speaker_bulb
    blue_pulse = 0x06                   #: bluetooth_speaker_bulb
    alarm = 0x07                        #: bluetooth_speaker_bulb
    flash = 0x08                        #: bluetooth_speaker_bulb
    breathing = 0x09                    #: bluetooth_speaker_bulb
    feel_green = 0x0a                   #: bluetooth_speaker_bulb
    sunsets = 0x0b                      #: bluetooth_speaker_bulb
    music = 0x0c                        #: bluetooth_speaker_bulb


class WhiteEffect(Enum):
    """
    An enum of white effects
    """
    white = 0x01
    naturelight = 0x02
    sunlight = 0x03
    sunset = 0x04
    candlelight = 0x05


class Effects(Enum):
    none = bytearray([SetLightFunction.effect.value, LightEffect.none.value])
    rainbow = bytearray(
        [SetLightFunction.effect.value, LightEffect.rainbow.value])
    flowing = bytearray(
        [SetLightFunction.effect.value, LightEffect.flowing.value])
    heartbeat = bytearray(
        [SetLightFunction.effect.value, LightEffect.heartbeat.value])
    red_pulse = bytearray(
        [SetLightFunction.effect.value, LightEffect.red_pulse.value])
    green_pulse = bytearray(
        [SetLightFunction.effect.value, LightEffect.green_pulse.value])
    blue_pulse = bytearray(
        [SetLightFunction.effect.value, LightEffect.blue_pulse.value])
    alarm = bytearray([SetLightFunction.effect.value, LightEffect.alarm.value])
    flash = bytearray([SetLightFunction.effect.value, LightEffect.flash.value])
    breathing = bytearray(
        [SetLightFunction.effect.value, LightEffect.breathing.value])
    feel_green = bytearray(
        [SetLightFunction.effect.value, LightEffect.feel_green.value])
    sunsets = bytearray(
        [SetLightFunction.effect.value, LightEffect.sunsets.value])
    music = bytearray([SetLightFunction.effect.value, LightEffect.music.value])

    white = bytearray(
        [SetLightFunction.white.value, WhiteEffect.white.value])
    naturelight = bytearray(
        [SetLightFunction.white.value, WhiteEffect.naturelight.value])
    sunlight = bytearray(
        [SetLightFunction.white.value, WhiteEffect.sunlight.value])
    sunset = bytearray(
        [SetLightFunction.white.value, WhiteEffect.sunset.value])
    candlelight = bytearray(
        [SetLightFunction.white.value, WhiteEffect.candlelight.value])


class SetTimerFunction(Enum):
    """
    An enum of all timer functions
    """
    auto_light_toggle_on = 0x16
    auto_light_toggle_off = 0x17
    auto_light_timer_start = 0x14
    auto_light_timer_stop = 0x15
    auto_music_toggle_on = 0x20
    auto_music_toggle_off = 0x21
    auto_music_timer_start = 0x18
    auto_music_timer_stop = 0x19
    alarm_1_toggle_on = 0x05
    alarm_1_toggle_off = 0x06
    alarm_1_time = 0x03
    alarm_2_toggle_on = 0x09
    alarm_2_toggle_off = 0x0a
    alarm_2_time = 0x07
    alarm_3_toggle_on = 0x0d
    alarm_3_toggle_off = 0x0e
    alarm_3_time = 0x0b


class GetTimerFunction(Enum):
    """
    An enum of all get timer functions
    """
    auto_music = 0x22
    auto_light = 0x23
    alarm_1 = 0x04
    alarm_2 = 0x08
    alarm_3 = 0x0c


class SetSpeakerFunction(Enum):
    """
    An enum of all speaker functions
    """
    speaker_effect = 0x05
    volume = 0x03
    frequency_80 = 0x0b
    frequency_200 = 0x0c
    frequency_500 = 0x0d
    frequency_2k = 0x0e
    frequency_8k = 0x0f


class GetSpeakerFunction(Enum):
    """
    An enum of all get speaker functions
    """
    volume = 0x04
    equalizer = 0x14


class SpeakerEffect(Enum):
    """
    An enum of all speaker equalizers
    """
    flat = 0x00
    classical = 0x01
    pop = 0x02
    bass = 0x03
    jazz = 0x04


class SpeakerEqualizerLevelMin(Enum):
    """
    An enum of spekar min
    """
    volume = 0x00
    frequency_80 = 0x15
    frequency_200 = 0x4d
    frequency_500 = 0x4f
    frequency_2k = 0x48
    frequency_8k = 0x48


class SpeakerEqualizerLevelMax(Enum):
    """
    An enum of spekar max
    """
    volume = 0x1f
    frequency_80 = 0x00
    frequency_200 = 0x09
    frequency_500 = 0x09
    frequency_2k = 0x0d
    frequency_8k = 0x0d


class SpeakerEffectEqualizer(Enum):
    """
    An enum of equalizer
    """
    flat = \
        {'frequency_80': 50, 'frequency_200': 50, 'frequency_500': 50,
            'frequency_2k': 50, 'frequency_8k': 50}
    classical = \
        {'frequency_80': 65, 'frequency_200': 67, 'frequency_500': 50,
            'frequency_2k': 29, 'frequency_8k': 68}
    pop = \
        {'frequency_80': 59, 'frequency_200': 50, 'frequency_500': 32,
            'frequency_2k': 57, 'frequency_8k': 80}
    bass = \
        {'frequency_80': 81, 'frequency_200': 66, 'frequency_500': 32,
            'frequency_2k': 51, 'frequency_8k': 68}
    jazz = \
        {'frequency_80': 72, 'frequency_200': 70, 'frequency_500': 61,
            'frequency_2k': 48, 'frequency_8k': 34}
