#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Unofficial Python API to control Alloyseed bulbs over Bluetooth
"""

__version__ = "0.0.8"


from alloyseed.bulb import Bulb
from alloyseed.connection import discover_alloyseed_lamps, find_device_by_address, model_from_name
from bleak import BleakError
from alloyseed.const import Effects