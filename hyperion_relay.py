#!/usr/bin/python3

"""
Uses a loopback serial connection on a Raspberry Pi to trigger a relay
breakout board connected to lightPin.
"""

import serial
import RPi.GPIO as GPIO
from time import sleep


# Set serial data; make sure baudrate is consistent with hyperion.
# To receive loopback serial data, place a jumper to short
# tx and rx GPIO pins.
loopback = serial.Serial(port='/dev/ttyS0', baudrate=38400)

# Assign GPIO BCM pins
lightPin, ledPower, ledPin = 2, 21, 3


def setup():
    """Set up GPIO and illuminate the status LED"""
    GPIO.setwarnings(False)

    # Use BCM pin numbering
    GPIO.setmode(GPIO.BCM)

    # Set GPIO pins as outputs
    for pin in (lightPin, ledPower, ledPin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.HIGH)


def read_from_hyperion():
    """Read and loopback serial data from hyperion"""
    incoming, message, preamble = False, [], [b'A', b'd', b'a', b'\x00', b'\x00', b'U']

    while True:
        try:
            data = loopback.read()

            if data:
                message.append(data)

                if incoming:
                    if len(message) >= 3:
                        # Assume the last three values are color values
                        yield message[-3:]

                        # Return to awaiting the preamble
                        incoming, message = False, []

                else:
                    if message == preamble:
                        # If preamble is received, the following data will be color values
                        incoming, message = True, []
                    elif len(message) > 6:
                        # If too many values are received, discard them
                        message = []

            del data

        except KeyboardInterrupt:
            # If user cancels with Ctrl+C, break the loop instead of exiting,
            # so GPIO can be cleaned up
            return

        sleep(.0001) # Sleep briefly to lower CPU usage


def process_color_data():
    """Process the received data to activate the lights"""
    on = True

    for message in read_from_hyperion():

        # Activate for any nonzero color value
        if not on and any(color > b'\x00' for color in message):
            on = switch_relay(True)

        # If all color values are zero, turn the relay off
        elif on and all(color == b'\x00' for color in message):
            on = switch_relay(False)


def switch_relay(on):
    if on:
        state = GPIO.LOW # Pulling the relay low turns it on
        status = True
    else:
        state = GPIO.HIGH # Pulling the relay pins high turns it off
        status = False
    GPIO.output(lightPin, state)
    print('Lights {}'.format('on' if status else 'off'))
    return status


def main():
    setup()

    # Flash the status LED twice to verify that the script is running
    for state in (GPIO.LOW, GPIO.HIGH) * 2:
        sleep(.25)
        GPIO.output(ledPin, state)

    # Loop to check for incoming color data and process it
    process_color_data()

    # Close serial connection
    print('Closing connection...')
    loopback.close()

    # Clean up GPIO
    GPIO.cleanup()


if __name__ == '__main__':
    main()
