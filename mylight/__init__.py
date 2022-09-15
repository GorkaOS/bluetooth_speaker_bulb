#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Unofficial Python API to control My Light bulbs over Bluetooth
"""

__version__ = "0.0.8"


from mylight.bulb import Bulb
from mylight.connection import discover_mylight_lamps, find_device_by_address, model_from_name
from bleak import BleakError
from mylight.const import Effects