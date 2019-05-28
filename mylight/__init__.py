#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Unofficial Python API to control My Light bulbs over Bluetooth
"""

__version__ = "0.0.1"

try:
    from mylight.mylightlib import MyLight
except ImportError:
    from mylightlib import MyLight

