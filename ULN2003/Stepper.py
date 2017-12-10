#!/usr/bin/python

#This class is to test the VERY basic functionality of stepping the 28BYJ-48 5v stepper motor using the ULN2008 motor controller

import sys
import time
import RPi.GPIO as GPIO
from LED.LEDs import LED
import threading
from Pin_Shutdown import Pins_Shutdown

GPIO.setmode(GPIO.BCM)

class Stepper:
    #Use BCM (Broadcom) pin references . These are universally understood (mostly) versus physical pin location
    #Define GPIO signals to use (Broadcom specification:

    def init_pins(self, motor_pins):
        GPIO.setmode(GPIO.BCM)
        for pin in motor_pins:
            print("Assigning pin {0} as OUT".format(pin))
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def rotate_clockwise_degree(self, motor_pins, sequence_speed=.001, degrees=90):
        #Set coil sequence for clockwise rotation. This is a 4 phase stepper motor, so 8 total steps in our sequence:
        sequence = [
                [1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 1]
            ]

        self.init_pins(motor_pins)
        sequence_steps = len(sequence)
        sequence_counter = 0
        degree_per_step = 0.087890625
        current_degree = degree_per_step
        try:
            GPIO.setmode(GPIO.BCM)
            sequence_count = 0
            print("Rotating {0} degrees clockwise...".format(degrees))
            while current_degree <= degrees:
                if (current_degree % 90.0) == 0:
                    print("Achieved {0} degrees".format(current_degree))
                    led_thread = threading.Thread(target=LED().ledTimed, args=(25, .5,))
                    led_thread.start()
                for pin in range(0, 4):
                    xpin = motor_pins[pin]
                    if sequence[sequence_counter][pin] != 0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                sequence_counter += 1

                if sequence_counter >= sequence_steps:
                    sequence_counter = 0
                current_degree += degree_per_step
                time.sleep(sequence_speed)
            print("Motor run complete. shutting down GPIO pins...")
            Pins_Shutdown().shutdown_pins(motor_pins)
        except KeyboardInterrupt:
            GPIO.cleanup()
        except Exception as e:
            print(e)
            print("Cleaning up GPIO pins...")
            GPIO.cleanup()
            print("Shutting down motor clean")

    def rotate_counter_clockwise_degree(self, motor_pins, sequence_speed=.001, degrees=90):
        #Set coil sequence for clockwise rotation. This is a 4 phase stepper motor, so 8 total steps in our sequence:
        sequence = [
                [0, 0, 0, 1],
                [0, 0, 1, 1],
                [0, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 1, 0, 0],
                [1, 1, 0, 0],
                [1, 0, 0, 1],
                [1, 0, 0, 1]
            ]
        self.init_pins(motor_pins)
        sequence_steps = len(sequence)
        sequence_counter = 0
        degree_per_step = 0.087890625
        current_degree = degree_per_step
        try:
            GPIO.setmode(GPIO.BCM)
            sequence_count = 0
            print("Rotating {0} degrees clockwise...".format(degrees))
            while current_degree <= degrees:
                if (current_degree % 90.0) == 0:
                    print("Achieved {0} degrees".format(current_degree))
                    led_thread = threading.Thread(target=LED().ledTimed, args=(25, .5,))
                    led_thread.start()
                for pin in range(0, 4):
                    xpin = motor_pins[pin]
                    if sequence[sequence_counter][pin] != 0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                sequence_counter += 1

                if sequence_counter >= sequence_steps:
                    sequence_counter = 0
                current_degree += degree_per_step
                time.sleep(sequence_speed)
            print("Motor run complete. shutting down GPIO pins...")
            Pins_Shutdown().shutdown_pins(motor_pins)
        except KeyboardInterrupt:
            GPIO.cleanup()
        except Exception as e:
            print(e)
            print("Cleaning up GPIO pins...")
            GPIO.cleanup()
            print("Shutting down motor clean")


