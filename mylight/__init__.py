#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Unofficial Python API to control My Light bulbs over Bluetooth
"""

__version__ = "0.0.2"



try:
    from mylight.bulb import Bulb, find_device_by_address, BleakError, discover_mylight_lamps, model_from_name
except ImportError:
    from mylight import Bulb, find_device_by_address, BleakError, discover_mylight_lamps, model_from_name