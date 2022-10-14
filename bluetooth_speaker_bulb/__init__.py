#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Unofficial Python API to control bluetooth speaker bulb
"""

__version__ = "0.0.13"


from bleak import BleakError

from .bulb import Bulb
from .connection import (discover_bluetooth_speaker_bulb_lamps,
                         find_device_by_address, model_from_name)
from .const import Effects
