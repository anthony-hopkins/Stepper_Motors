#!/usr/bin/python

#This class is to test the VERY basic functionality of stepping the 28BYJ-48 5v stepper motor using the ULN2008 motor controller

import sys
import time
import RPi.GPIO as GPIO
from led_testing.LEDtest import TestLED
import threading
GPIO.setmode(GPIO.BCM)

class TestStepper:
    #Use BCM (Broadcom) pin references . These are universally understood (mostly) versus physical pin location
    #Define GPIO signals to use:
    #Physical pins: 11, 15, 16, 18
    #Broadcom pin references: GPIO0, GPIO3, GPIO4, GPIO5
    step_pins = [17, 22, 23, 24]
    motor_led_pin = 25

    #Assign all involved pins as OUTPUT since we are only talking to the motor controller. This is a one-way conversation

    simple_step_counter = 0
    simple_steps = 4
    simple_sequence = range(0, 4)
    simple_sequence[0] = [1, 0, 0, 0]
    simple_sequence[1] = [0, 1, 0, 0]
    simple_sequence[2] = [0, 0, 1, 0]
    simple_sequence[3] = [0, 0, 0, 1]

    reverse_step_counter = 0
    reverse_steps = 8
    reverse_sequence = range(0, 8)
    reverse_sequence[0] = [0, 0, 0, 1]
    reverse_sequence[1] = [0, 0, 1, 1]
    reverse_sequence[2] = [0, 0, 1, 0]
    reverse_sequence[3] = [0, 1, 1, 0]
    reverse_sequence[4] = [0, 1, 0, 0]
    reverse_sequence[5] = [1, 1, 0, 0]
    reverse_sequence[6] = [1, 0, 0, 0]
    reverse_sequence[7] = [1, 0, 0, 1]
    

    advanced_step_counter = 0
    advanced_steps = 8
    advanced_sequence = range(0, 8)
    advanced_sequence[0] = [1, 0, 0, 0]
    advanced_sequence[1] = [1, 1, 0, 0]
    advanced_sequence[2] = [0, 1, 0, 0]
    advanced_sequence[3] = [0, 1, 1, 0]
    advanced_sequence[4] = [0, 0, 1, 0]
    advanced_sequence[5] = [0, 0, 1, 1]
    advanced_sequence[6] = [0, 0, 0, 1]
    advanced_sequence[7] = [1, 0, 0, 1]


    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for pin in self.step_pins:
            print("Assigning pin {0} as OUT".format(pin))
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def rotate_clockwise_degree(self, sequence_speed=.001, degrees=90):
        degree_per_step = 0.087890625
        current_degree = degree_per_step
        try:
            GPIO.setmode(GPIO.BCM)
            sequence_count = 0
            print("Rotating {0} degrees clockwise...".format(degrees))
            while current_degree <= degrees:
                if (current_degree % 90.0) == 0:
                    print("Achieved {0} degrees".format(current_degree))
                    led_thread = threading.Thread(target=TestLED().ledTimed, args=(25, .5,))
                    led_thread.start()
                for pin in range(0, 4):
                    xpin = self.step_pins[pin]
                    if self.advanced_sequence[self.advanced_step_counter][pin] != 0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                self.advanced_step_counter += 1

                if self.advanced_step_counter >= self.advanced_steps:
                    self.advanced_step_counter = 0
                if self.advanced_step_counter < 0:
                    self.advanced_step_counter = self.advanced_steps
                current_degree += degree_per_step
                time.sleep(sequence_speed)
            print("Motor run complete. shutting down GPIO pins...")
        except KeyboardInterrupt:
            GPIO.cleanup()
        except Exception as e:
            print(e)
            #print("Cleaning up GPIO pins...")
            #GPIO.cleanup()
            #print("Shutting down motor clean")

    def rotate_counter_clockwise_degree(self, sequence_speed=.001, degrees=90):
        degree_per_step = 0.087890625
        current_degree = degree_per_step
        try:
            GPIO.setmode(GPIO.BCM)
            sequence_count = 0
            print("Rotating {0} degrees clockwise...".format(degrees))
            while current_degree <= degrees:
                if (current_degree % 90.0) == 0:
                    print("Achieved {0} degrees".format(current_degree))
                    led_thread = threading.Thread(target=TestLED().ledTimed, args=(25, .5,))
                    led_thread.start()
                for pin in range(0, 4):
                    xpin = self.step_pins[pin]
                    if self.reverse_sequence[self.reverse_step_counter][pin] != 0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                self.reverse_step_counter += 1

                if self.reverse_step_counter >= self.reverse_steps:
                    self.reverse_step_counter = 0
                if self.reverse_step_counter < 0:
                    self.reverse_step_counter = self.reverse_steps
                current_degree += degree_per_step
                time.sleep(sequence_speed)
            print("Motor run complete. shutting down GPIO pins...")
        except KeyboardInterrupt:
            GPIO.cleanup()
        except Exception as e:
            print(e)
           #print("Cleaning up GPIO pins...")
           #GPIO.cleanup()
           #print("Shutting down motor clean")
        

#GPIO.setwarnings(False)
#TestStepper().rotate_clockwise(.001, 4.595)
#4.62 is the sweet spot for sequencially running counter-clockwise after a clockwise rotation:
#TestStepper().rotate_counter_clockwise(.001, 4.595)
TestStepper().rotate_clockwise_degree(.001, 360)
TestStepper().rotate_counter_clockwise_degree(.001, 360)
