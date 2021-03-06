#!/usr/bin/python

#This class is to test the VERY basic functionality of stepping the 28BYJ-48 5v stepper motor using the ULN2008 motor controller

import threading
import time
import RPi.GPIO as GPIO
from Pin_Shutdown import Pins_Shutdown
from LED.LEDs import LED
GPIO.setmode(GPIO.BCM)

class Stepper:
    #Assigning class attributes since we are using stepper motors with static values associated with them
    sequence_steps = 8
    degree_per_step = 0.087890625
    forward_sequence = [
                [1, 0, 0, 0],
                [1, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1],
                [0, 0, 0, 1],
                [1, 0, 0, 1]
                ]
    reverse_sequence = [
                [0, 0, 0, 1],
                [0, 0, 1, 1],
                [0, 0, 1, 0],
                [0, 1, 1, 0],
                [0, 1, 0, 0],
                [1, 1, 0, 0],
                [1, 0, 0, 0],
                [1, 0, 0, 1]
                ]

    def init_pins(self, motor_pins):
        GPIO.setmode(GPIO.BCM)
        for pin in motor_pins:
            print("Assigning pin {0} as OUT".format(pin))
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def rotate(self, direction, motor_pins, sequence_speed=.001, degrees=90):
        self.init_pins(motor_pins)
        #Set coil sequence for clockwise rotation. This is a 4 phase stepper motor, so 8 total steps in our sequence:
        if direction == "clockwise" or direction != "counter-clockwise":
            sequence = self.forward_sequence
        else:
            sequence = self.reverse_sequence
        sequence_counter = 0
        current_degree = self.degree_per_step
        try:
            GPIO.setmode(GPIO.BCM)
            sequence_count = 0
            print("Rotating {0} degrees clockwise...".format(degrees))
            while current_degree <= degrees:
                if (current_degree % 90.0) == 0:
                    print("Achieved {0} degrees".format(current_degree))
                    led_thread = threading.Thread(target=LED().ledTimed, args=(21, .5,))
                    led_thread.start()
                for pin in range(0, 4):
                    xpin = motor_pins[pin]
                    if sequence[sequence_counter][pin] != 0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                sequence_counter += 1

                if sequence_counter >= self.sequence_steps:
                    sequence_counter = 0
                current_degree += self.degree_per_step
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


