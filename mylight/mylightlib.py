#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# =============================================================================
# title           : mylightlib.py
# description     : Python library to control My Light bulbs over Bluetooth
#                   Based on magicbluelib.py by Benjamin Piouffle
# author          : Oskar Joelsson
# date            : 18/01/2019
# python_version  : 3.7.2
# =============================================================================
import functools
import logging
import random
from enum import Enum

from bluepy import btle

__all__ = ['MyLight', 'Effect']

logger = logging.getLogger(__name__)

UUID_CHARACTERISTIC_RECV = btle.UUID('a041')
UUID_CHARACTERISTIC_WRITE = btle.UUID('a040')
UUID_CHARACTERISTIC_DEVICE_NAME = btle.UUID('2a00')

ON = 0x01
OFF = 0x00
REQ_DATA = 0x06


class SetBulbCategory(Enum):
    """
    An enum of all set catagories
    """
    sound = 0x04
    timer = 0x05
    lamp = 0x08
    state = 0x0b


class GetBulbCategory(Enum):
    """
    An enum of all get catagories
    """
    sound = 0x84
    timer = 0x85
    lamp = 0x88
    state = 0x8b


class SetLampFunction(Enum):
    """
    An enum of all set lamp functions
    """
    brightness = 0x01
    color = 0x02
    power = 0x05
    effect = 0x06
    white_intensity = 0x07
    white_effect = 0x09


class GetLampFunction(Enum):
    """
    An enum of all get lamp functions
    """
    # status = 0x16
    color = 0x15


class Effect(Enum):
    """
    An enum of all the possible effects the bulb can accept
    """
    rainbow = 0x01                      #: mylight
    flowing = 0x02                      #: mylight
    heartbeat = 0x03                    #: mylight
    red_pulse = 0x04                    #: mylight
    green_pulse = 0x05                  #: mylight
    blue_pulse = 0x06                   #: mylight
    alarm = 0x07                        #: mylight
    flash = 0x08                        #: mylight
    breathing = 0x09                    #: mylight
    feel_green = 0x0a                   #: mylight
    sunset = 0x0b                       #: mylight
    music = 0x0c                        #: mylight


class WhiteEffect(Enum):
    """
    An enum of white effects
    """
    white = 0x01
    naturelight = 0x02
    sunlight = 0x03
    sunset = 0x04
    candlelight = 0x05


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


class SetSoundFunction(Enum):
    """
    An enum of all sound functions
    """
    volume_level = 0x03
    sound_effect = 0x05
    eq_80_level = 0x0b
    eq_200_level = 0x0c
    eq_500_level = 0x0d
    eq_2k_level = 0x0e
    eq_8k_level = 0x0f


class GetSoundFunction(Enum):
    """
    An enum of all get sound functions
    """
    volume = 0x04
    eq = 0x14


class SoundEffect(Enum):
    """
    An enum of all sound equalizers
    """
    flat = 0x00
    classical = 0x01
    pop = 0x02
    bass = 0x03
    jazz = 0x04


def connection_required(func):
    """Raise an exception before calling the actual function if the device is
    not connected.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._connection is None:
            raise Exception("Not connected")

        return func(self, *args, **kwargs)

    return wrapper


def _figure_addr_type(mac_address=None, addr_type=None):
    # addr_type rules all
    if addr_type is not None:
        return addr_type

    # try using mac_address
    if mac_address is not None:
        mac_address_num = int(mac_address.replace(':', ''), 16)
        if mac_address_num & 0xF00000000000 == 0xF00000000000:
            return btle.ADDR_TYPE_PUBLIC

    return btle.ADDR_TYPE_PUBLIC


class MyLight():
    """
    Class to interface with Magic Blue light
    """

    def __init__(self, mac_address, adapter=0, addr_type=None):
        """
        :param mac_address: device MAC address as a string
        :param version: bulb version as displayed in official app (integer)
        """
        self._connection = None

        self.mac_address = mac_address
        self._adapter = adapter
        self._addr_type = _figure_addr_type(mac_address, addr_type)

        self._device_info = {}
        self._timer_info = {}
        self._sound_info = {}

        self._is_on = None
        self._brightness = None
        self._rgb_color = [0, 0, 0]
        self._effect = None
        self._effects = Effect
        self._white_intensity = None

    @property
    def effects(self):
        """Return effects Enum """
        return self._effects

    @property
    def is_on(self):
        """Return on or off"""
        return self._device_info['on']

    @property
    def rgb_color(self):
        """Return the color property as list of [R, G, B], each 0-255."""
        return self._device_info['rgb_color']

    @property
    def brightness(self):
        """Return the brightness level."""
        return self._device_info['brightness']

    @property
    def effect(self):
        """Return which effect """
        try:
            data = self._device_info['effect']
        except KeyError:
            return None
        return data

    @property
    def effect_value(self):
        """Return which effect value """
        try:
            data = self._device_info['effect'].value
        except KeyError:
            return None
        return data


    @property
    def effect_name(self):
        """Return which effect """
        try:
            data = self._device_info['effect'].name
        except KeyError:
            return None
        return data


    @property
    def white_intensity(self):
        """Return if white is on or off"""
        return self._device_info['warm']

    def connect(self):
        """
        Connect to device

        :param adapter: bluetooth adapter name as shown by            "hciconfig" command. Default : 0 for (hci0)

        :return: True if connection succeed, False otherwise
        """
        logger.debug("Connecting...")
        retries = 5
        for attempt in range(1, retries + 1, 1):
            logger.info('Connection attempt: {}'.format(attempt))
            try:
                connection = btle.Peripheral(self.mac_address, self._addr_type,
                                             self._adapter)
                self._connection = connection.withDelegate(self)
                self._subscribe_to_recv_characteristic()
            except btle.BTLEException as e:
                if e.code != btle.BTLEException.DISCONNECTED:
                    raise
            # except RuntimeError as e:
            #     logger.error('Connection failed: {}'.format(e))
            #     raise
            else:
                logger.info(
                    'Successfully connected to: {}'.format(self.mac_address))
                break

            if attempt == retries:
                logger.error('Connection failed: {}'.format(self.mac_address))
                return False
        self.update(['lamp', 'sound', 'timer'])
        return True

    def disconnect(self):
        """
        Disconnect from device
        """
        logger.debug("Disconnecting...")

        try:
            self._connection.disconnect()
        except btle.BTLEException:
            pass

        self._connection = None

    def is_connected(self):
        """
        :return: True if connected
        """
        return self._connection is not None

    def test_connection(self):
        """
        Test if the connection is still alive

        :return: True if connected
        """
        if not self.is_connected():
            return False

        # send test message, read bulb name
        try:
            self.get_device_name()
        except btle.BTLEException:
            self.disconnect()
            self._device_info = None
            self._timer_info = None
            self._sound_info = None
            return False
        except BrokenPipeError:
            # bluepy-helper died
            self._connection = None
            self._device_info = None
            self._timer_info = None
            self._sound_info = None
            return False

        return True

    # Read from bulb
    @connection_required
    def get_device_name(self):
        """
        :return: Device name
        """
        buffer = self._device_name_characteristic.read()
        buffer = buffer.replace(b'\x00', b'')
        return buffer.decode('ascii')

    @connection_required
    def get_device_info(self):
        """
        Retrieve device info for shell
        """
        msg = Protocol.encode_msg(SetBulbCategory.lamp.value,
                                  GetLampFunction.color.value,
                                  REQ_DATA)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, withResponse=True)
        buffer = self._connection.readCharacteristic(0x000e)
        logger.debug("Buffer received: " + str(buffer))
        self._device_info = Protocol.decode_lamp_info(buffer)
        logger.debug("Decode received: " + str(self._device_info))
        return self._device_info

    @connection_required
    def update(self, categories=['lamp']):
        """
        Retrieve device info

        :param categories: list which categories to receive
        """

        for category in categories:
            c = SetBulbCategory[category]
            if c == SetBulbCategory.lamp:
                self._device_info = \
                    self.get_category_info(c, GetLampFunction)[0]
            elif c == SetBulbCategory.timer:
                self._timer_info = self.get_category_info(c, GetTimerFunction)
            elif c == SetBulbCategory.sound:
                self._sound_info = self.get_category_info(c, GetSoundFunction)
            else:
                return False
        return True

    def get_category_info(self, category, functions, with_response=True):
        """
        Retrieve category in from all functions.

        :param category: category to retrieve info from
        :param functions: functions to retrieve info from
        """
        buffer_list = []
        for func in functions:
            msg = Protocol.encode_msg(category.value,
                                      func.value,
                                      REQ_DATA)
            msg.append(Protocol.encode_checksum(msg))
            self._send_characteristic.write(msg, withResponse=True)
            buffer = self._connection.readCharacteristic(0x000e)
            buffer_list.append(self.decode_function(buffer))
        return buffer_list

    def decode_function(self, buffer):
        """
        Retrieve

        :param buffer: buffer to decode not pretty
        """
        if len(buffer) < 1:
            return []
        c = buffer[3]
        f = buffer[4]

        if c == GetBulbCategory.lamp.value:
            if f == GetLampFunction.color.value:
                return Protocol.decode_lamp_info(buffer)

        if c == GetBulbCategory.timer.value:
            if f == GetTimerFunction.auto_light.value \
                    or f == GetTimerFunction.auto_music.value:
                return Protocol.decode_time_auto(buffer)

            if f == GetTimerFunction.alarm_1.value \
                    or f == GetTimerFunction.alarm_2.value \
                    or f == GetTimerFunction.alarm_3.value:
                return Protocol.decode_time_alarm(buffer)

        if c == GetBulbCategory.sound.value:
            if f == GetSoundFunction.volume.value:
                return Protocol.decode_sound_volume(buffer)

            if f == GetSoundFunction.eq.value:
                return Protocol.decode_sound_equlizer(buffer)

        return []

    # Lamp
    @connection_required
    def turn_off(self, with_response=True):
        """
        Turn off the light
        """
        msg = Protocol.encode_msg(SetBulbCategory.lamp.value,
                                  SetLampFunction.power.value,
                                  OFF)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, with_response)

    @connection_required
    def turn_on(self, brightness=None, with_response=True):
        """
        Set white color on the light

        :param brightness: a float value between 0.0 and 1.0 defining the
            brightness
        """
        msg = Protocol.encode_msg(SetBulbCategory.lamp.value,
                                  SetLampFunction.power.value,
                                  ON)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, with_response)
        if brightness is not None:
            self.set_brightness(brightness)
        else:
            self.set_brightness(255)

    @connection_required
    def set_white_intensity(self, intensity, with_response=True):
        """
        Set white intensity

        ;param intensity: value between 1..255
        """
        msg = Protocol.encode_msg(SetBulbCategory.lamp.value,
                                  SetLampFunction.white_intensity.value,
                                  intensity)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, with_response)

    @connection_required
    def set_brightness(self, brightness, with_response=True):
        """
        Set Brightness

        :param intensity: brightness between 1..255
        """
        msg = Protocol.encode_msg(SetBulbCategory.lamp.value,
                                  SetLampFunction.brightness.value,
                                  brightness)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, with_response)

    @connection_required
    def set_rgb_color(self, rgb_color, with_response=True):
        """
        Change bulb's color

        :param rgb_color: color as a list of 3 values between 0 and 255
        """
        msg = Protocol.encode_msg(SetBulbCategory.lamp.value,
                                  SetLampFunction.color.value,
                                  rgb_color)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, with_response)

    @connection_required
    def set_random_color(self):
        """
        Change bulb's color with a random color
        """
        self.set_rgb_color([random.randint(1, 255) for i in range(3)])

    @connection_required
    def set_effect(self, effect, with_response=True):
        """
        Set an effect

        :param effect: An effect
        """
        msg = Protocol.encode_msg(SetBulbCategory.lamp.value,
                                  SetLampFunction.effect.value,
                                  Effect[effect].value)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, with_response)

    @connection_required
    def set_white(self, with_response=True):
        """
        Set white

        """
        msg = Protocol.encode_msg(SetBulbCategory.lamp.value,
                                  SetLampFunction.white_effect.value,
                                  ON)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, with_response)

    # Timer
    @connection_required
    def turn_off_timer(self, toggle_no, with_response=True):
        """
        Turn off the timer toggles

        :param toggle: An toggle (see :class:`.SetTimerFunction`)
        """
        toggle = toggle_no.value
        msg = Protocol.encode_msg(SetBulbCategory.sound.value,
                                  toggle)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, with_response)

    @connection_required
    def turn_on_timer(self, toggle_no, with_response=True):
        """
        Turn off the timer toggles

        :param toggle: An toggle (see :class:`.SetTimerFunction`)
        """
        toggle = toggle_no.value
        msg = Protocol.encode_msg(SetBulbCategory.sound.value,
                                  toggle)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, with_response)

    # Sound
    @connection_required
    def set_sound_level(self, level, sound_function_no=3,
                        with_response=True):
        """
        Set sound levels for volume and equalizer

        :param level: The level for the sound function. Between 0 and 100
        :param sound_function: An sound function\
        ;(see :class:`.SetSoundFunction`)
        """
        min_level = 0x4f
        level_modified = int(level * (min_level/100))
        msg = Protocol.encode_msg(SetBulbCategory.sound.value,
                                  sound_function_no,
                                  level_modified)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, with_response)

    @connection_required
    def set_sound_effect(self, sound_effect_no, with_response=True):
        """
        Set sound effect, flat, classical, pop, bass, jazz

        :param sound_effect: An sound effect (see :class:`.SoundEffect`)
        """
        sound_effect = sound_effect_no.value
        msg = Protocol.encode_msg(SetBulbCategory.sound.value,
                                  SetSoundFunction.sound_effect.value,
                                  sound_effect)
        msg.append(Protocol.encode_checksum(msg))
        self._send_characteristic.write(msg, with_response)

    @property
    def _send_characteristic(self):
        """Get BTLE characteristic for sending commands"""
        characteristics = self._connection.getCharacteristics(
            uuid=UUID_CHARACTERISTIC_WRITE)
        if not characteristics:
            return None
        return characteristics[0]

    @property
    def _recv_characteristic(self):
        """Get BTLE characteristic for receiving data"""
        characteristics = self._connection.getCharacteristics(
            uuid=UUID_CHARACTERISTIC_RECV)
        if not characteristics:
            return None
        return characteristics[0]

    @property
    def _device_name_characteristic(self):
        """Get BTLE characteristic for reading device name"""
        characteristics = self._connection.getCharacteristics(
            uuid=UUID_CHARACTERISTIC_DEVICE_NAME)
        if not characteristics:
            return None
        return characteristics[0]

    @property
    def _device_info_characteristic(self):
        """Get BTLE characteristic for reading device name"""
        characteristics = self._connection.getCharacteristics(
            uuid=UUID_CHARACTERISTIC_RECV)
        if not characteristics:
            return None
        return characteristics[0]

    def _subscribe_to_recv_characteristic(self):
        char = self._recv_characteristic
        handle = char.valHandle - 4
        msg = bytearray([0x01, 0x00])
        self._connection.writeCharacteristic(handle, msg, withResponse=True)

    def __str__(self):
        return "<MyLight({})>".format(self.mac_address)


class Protocol():
    """
    Protocol encoding/decoding for the bulb
    """

    # Encode
    # Message
    @staticmethod
    def encode_msg(category, function, data=[]):
        """
        Construct a message

        :param category: category to use
        :param function: function to use
        :param data: int, list or tuple, data for function
        :return: encoded msg
        """
        if isinstance(data, int):
            # Only one int as data, put in list, length will be 1
            data = [data]
        msg = bytearray([0x55, 0xaa, len(data), category, function])
        for d in data:
            msg.append(d)
        logger.debug("msg: " + str(msg))
        return msg

    # Checksum
    @staticmethod
    def encode_checksum(msg):
        """
        Construct checksum for msg to send

        :param msg: encoded message
        :return: checksum
        """
        checksum_multiple = 256  # 0x100
        hex_sum = sum(i for i in msg) + 1
        return ((checksum_multiple * len(msg)) - hex_sum) % checksum_multiple

    # Decode
    # Lamp
    @staticmethod
    def decode_lamp_info(buffer):
        """
        Decode a message with device info

        :param buffer: buffer to decode

        Lamp package
        0:  55  header
        1:  aa  header
        2:  09  data lenght
        3:  88  Catagory (88 lamp receive, 08 lamp send)
        4:  15  Function
        5:  00  R
        6:  00  G
        7:  00  B
        8:  75  white intensity cold (8 + 9, (7*16+5)+(8*16+a) = 0xff)
        9:  8a  white intensity warm (8 + 9, (7*16+5)+(8*16+a) = 0xff)
        10: 8d  brightness
        11: 01  on/off
        12: 00  effect
        13: 50  ?
        14: 7d  checksum
        """
        info = {
            'r':            buffer[5],
            'g':            buffer[6],
            'b':            buffer[7],
            'cold':         buffer[8],
            'warm':         buffer[9],
            'brightness':   buffer[10],
            'on':           buffer[11],
            'effect_no':    buffer[12],
            'rgb_color':    [buffer[5], buffer[6], buffer[7]],
        }
        if int(info['effect_no']) > 0:
            try:
                effect_no = int(info['effect_no'] - 1)
                info['effect'] = Effect(effect_no)
            except ValueError:
                pass

        return info

    # Timer
    @staticmethod
    def decode_time_auto(buffer):
        """
        Decode a message with device info

        :param buffer: buffer to decode

        Timer package
        0:  55  header
        1:  aa  header
        2:  05  data lenght
        3:  85  Catagory (85 timer receive, 08 timer send)
        4:  23  Function (auto light 23, auto music 22)
        5:  00  on/off
        6:  0c  start hour
        7:  00  start minute
        8:  0c  stop hour
        9:  00  stop minute
        10: 3b  checksum
        """
        info = {
            'function':     buffer[4],
            'on':           buffer[5],
            'start_hour':   buffer[6],
            'start_minut':  buffer[7],
            'stop_hour':    buffer[8],
            'stop_minute':  buffer[9],
        }
        return info

    @staticmethod
    def decode_time_alarm(buffer):
        """
        Decode a message with device info

        :param buffer: buffer to decode

        Timer package
        0:  55  header
        1:  aa  header
        2:  0a  data lenght
        3:  85  Catagory (85 timer receive, 08 timer send)
        4:  04  Function (04 alarm1, 08 alarm2, 0c alarm3)
        5:  00  ?
        6:  14  ?
        7:  10  ?
        8:  01  ?
        9:  01  ?
        10: 01  ?
        11: 06  hour
        12: 2d  minute
        13: 00  ?
        14: 01  on/off
        15: 12  checksum
        """
        info = {
            'alarm_no':     buffer[4],
            'alarm_hour':   buffer[11],
            'alarm_minute': buffer[12],
            'alarm_on':     buffer[14],
        }
        return info

    # Sound
    @staticmethod
    def decode_sound_volume(buffer):
        """
        Decode a message with device info

        :param buffer: buffer to decode

        Sound package
        0:  55  header
        1:  aa  header
        2:  01  data lenght
        3:  84  Catagory (84 sound receive, 08 sound send)
        4:  04  Function (volume)
        5:  20  volume
        6:  57  checksum
        """
        info = {
            'volume':       buffer[5],
        }
        return info

    @staticmethod
    def decode_sound_equlizer(buffer):
        """
        Decode a message with device info

        :param buffer: buffer to decode

        Sound package
        0:  55  header
        1:  aa  header
        2:  01  data lenght
        3:  84  Catagory (84 sound receive, 08 sound send)
        4:  14  Function (equlizer)
        5:  32  80_level
        6:  32  200_level
        7:  32  500_level
        8:  32  2k_level
        9:  32  8k_level
        10: 69  checksum
        """
        info = {
            '80_level': buffer[5],
            '200_level': buffer[6],
            '500_level': buffer[7],
            '2k_level': buffer[8],
            '8k_level': buffer[9],
        }
        return info

    # Checksum
    @staticmethod
    def verify_received_checksum(msg, encoded_checksum):
        """
        Verify checksum from received msg

        :param msg: complete message
        :param checksum: received encode_checksum(msg[0:-1])
        :return: true or false, if checksum received is the same as calculated.
        """
        return msg[-1] == encoded_checksum
