#!/usr/bin/python3

"""
Activate a relay breakout board when color data is sent to hyperion.
This can be used to control incandescent lights or any non-LED device
using hyperion.
"""

from collections import deque
import RPi.GPIO as GPIO
from serial import Serial, SerialException
from time import sleep


# Assign GPIO BCM pins
relayPin, ledPower, ledPin = 2, 21, 3
# Assign virtual serial port set by hyperion-loopback systemd service
ser = Serial('/etc/hyperion/hyperion_read')


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


def read_serial():
    """
    Read loopback serial data from hyperion and determine whether
    color data is being sent.  Once the preamble is stripped from
    the message, the last three bytes contain RGB color information.
    If all three are zero, yield False.  If any of the three are
    greater than zero, yield True to the calling function.
    """
    message, preamble = deque(maxlen=9), [b'A', b'd', b'a', b'\x00', b'\x00', b'U']
    while True:
        try:
            data = ser.read()
        except SerialException:
            pass
        else:
            message.append(data)
            if len(message) is 9 and [message[i] for i in range(6)] == preamble:
                payload = [message[i] for i in range(6, 9)]
                if all(i == b'\x00' for i in payload):
                    yield False
                else:
                    yield True
        sleep(.001)


def switch_relay(state):
    """
    Switch the relay based on the input command, then return the changed state.
    Pulling the relay pin low activates it, while pulling high deactivates it.
    """
    GPIO.output(relayPin, not state)
    print('Lights {}'.format('on' if state else 'off'))
    return state


def run():
    """Send received serial data to the relay when state changes"""
    last = None
    for signal in read_serial():
        if signal != last:
            last = switch_relay(signal)


if __name__ == '__main__':
    setup()
    # Flash the status LED twice to verify that the script is running
    for state in (0, 1) * 2:
        sleep(.25)
        GPIO.output(ledPin, state)
    try:
        run() # Loop to check for color data and process it
    finally:
        ser.close() # Close serial connection
        GPIO.cleanup() # Clean up GPIO
