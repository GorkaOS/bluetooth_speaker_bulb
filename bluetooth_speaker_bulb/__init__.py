#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Unofficial Python API to control bluetooth speaker bulb
"""

__version__ = "0.0.11"


from bluetooth_speaker_bulb.bulb import Bulb
from bluetooth_speaker_bulb.connection import discover_bluetooth_speaker_bulb_lamps, find_device_by_address, model_from_name
from bleak import BleakError
from bluetooth_speaker_bulb.const import Effects