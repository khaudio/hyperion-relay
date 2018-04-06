#!/usr/bin/python3

"""
Activate the relay, then exit.  This script will not wait for new commands.
"""

from hyperion_relay import setup, switch_relay


setup()
switch_relay(True)
