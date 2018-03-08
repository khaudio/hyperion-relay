#!/usr/bin/python3

"""
Activate a relay breakout board when color data is sent to hyperion.
This can be used to control incandescent lights or any non-LED device
using hyperion.
"""

from re import search
from subprocess import Popen, PIPE
from time import sleep
import RPi.GPIO as GPIO


# Assign GPIO BCM pins
relayPin, ledPower, ledPin = 2, 21, 3


def setup():
    """
    Set up GPIO and illuminate the status LED
    """
    GPIO.setwarnings(False)

    # Use BCM pin numbering
    GPIO.setmode(GPIO.BCM)

    # Set GPIO pins as outputs
    for pin in (relayPin, ledPower, ledPin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)


def run():
    """
    Check hyperion for color information via a subprocess call, then
    activate the relay if data is found.

    Pulling the relay pin low activates it, while pulling high deactivates it.
    """
    on = False

    while True:
        status = Popen(['hyperion-remote', '-l'], stdout=PIPE).stdout.read().decode('utf-8')
        signal = search('(?<=HEX\sValue"\s:\s\[\s").+(?="\s],)', status)

        if signal and not on:
            on = switch_relay(0) # Activate the relay

        elif not signal and on:
            on = switch_relay(1) # Deactivate the relay

        sleep(.01) # Sleep briefly to lower CPU usage


def switch_relay(state):
    """
    Switch the relay based on the input command, then return the changed state.
    """
    GPIO.output(relayPin, state)
    print('Lights {}'.format('off' if state else 'on'))
    return not state


if __name__ == '__main__':
    setup()

    # Flash the status LED twice to verify that the script is running
    for state in (0, 1) * 2:
        sleep(.25)
        GPIO.output(ledPin, state)

    try:
        run() # Loop to check for color data and process it

    finally:
        GPIO.cleanup() # Clean up GPIO
