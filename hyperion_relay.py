#!/usr/bin/python3

import serial
import RPi.GPIO as GPIO
from time import sleep


ser = serial.Serial(port='/dev/ttyS0', baudrate=38400)

GPIO.setwarnings(False)

# Assign GPIO BCM pins
ledPower = 21
lightPin = 2
ledPin = 3

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPower, GPIO.OUT)
GPIO.setup(lightPin, GPIO.OUT)
GPIO.setup(ledPin, GPIO.OUT)

# Set GPIO pins as outputs
GPIO.output(ledPower, GPIO.HIGH)
GPIO.output(lightPin, GPIO.HIGH)
GPIO.output(ledPin, GPIO.HIGH)

# Set default values
state = True
prefix = [65, 100, 97, 0, 0, 85]
lightsOff = [0, 0, 0]
message = []

'''Flash the status LED twice to visually verify that the script is running'''
for i in range(2):
    sleep(.25)
    GPIO.output(ledPin, GPIO.LOW)
    sleep(.25)
    GPIO.output(ledPin, GPIO.HIGH)

'''Read the loopback data from hyperion and process it'''
while True:
    try:
	# Read raw serial data
        data = bytes(ser.read())
        if data:
            for i in data:
                message.append(i)
	# Verify that the serial message is in the correct format
        if len(message) == 9 and message[:6] == prefix:
	    # Print the serial data for debugging purposes
            print(message)
            if message[-3:] == lightsOff:
		# Set state to FALSE so we know when to turn it on
                state = False
		# A state of HIGH means the relay is off
                GPIO.output(lightPin, GPIO.HIGH)
                print('Lights off')
	    # Only turn the lights on if it is currently off; do not attempt to bring lightPin LOW when it is already low
            elif not state:
                state = True
		# Bringing the lightPin LOW turns it on
                GPIO.output(lightPin, GPIO.LOW)
                print('Lights on')
	    # Forget serial data to read again
            message = []
    # If user cancels with Ctrl+C, break the loop instead of exiting so GPIO can be cleaned up
    except KeyboardInterrupt:
        break
    sleep(.001)
# Clean up GPIO
GPIO.cleanup()
print('Closing connection...')
ser.close()
