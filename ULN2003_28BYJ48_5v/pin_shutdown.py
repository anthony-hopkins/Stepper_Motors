#!/usr/bin/python

#This class is to test the VERY basic functionality of stepping the 28BYJ-48 5v stepper motor using the ULN2008 motor controller

import sys
import time
import RPi.GPIO as GPIO

#Use BCM (Broadcom) pin references . These are universally understood (mostly) versus physical pin location
GPIO.setmode(GPIO.BCM)

#Turn off warnings since this is a raw shutdown:
GPIO.setwarnings(False)
#Define GPIO signals to use:
#Physical pins: 11, 15, 16, 18
#Broadcom pin references: GPIO0, GPIO3, GPIO4, GPIO5
step_pins = [17, 22, 23, 24]

#Assign all involved pins as OUTPUT since we are only talking to the motor controller. This is a one-way conversation
for pin in step_pins:
    print("Assigning pin {0} as OUT".format(pin))
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

