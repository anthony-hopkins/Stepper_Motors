#!/usr/bin/python

#This class is to test the VERY basic functionality of stepping the 28BYJ-48 5v stepper motor using the ULN2008 motor controller

import sys
import time
import RPi.GPIO as GPIO

#Use BCM (Broadcom) pin references . These are universally understood (mostly) versus physical pin location
GPIO.setmode(GPIO.BCM)

#Turn off warnings since this is a raw shutdown:
GPIO.setwarnings(False)

#Assign all involved pins as OUTPUT since we are only talking to the motor controller. This is a one-way conversation
class Pins_Shutdown:

    def shutdown_pins(self, pins):
        for pin in pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
