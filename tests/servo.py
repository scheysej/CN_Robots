#  ___   ___  ___  _   _  ___   ___   ____ ___  ____  
# / _ \ /___)/ _ \| | | |/ _ \ / _ \ / ___) _ \|    \ 
#| |_| |___ | |_| | |_| | |_| | |_| ( (__| |_| | | | |
# \___/(___/ \___/ \__  |\___/ \___(_)____)___/|_|_|_|
#                  (____/ 
# Osoyoo Model-Pi L298N DC motor driver programming guide
# tutorial url: https://osoyoo.com/2020/03/01/python-programming-tutorial-model-pi-l298n-motor-driver-for-raspberry-pi/

from __future__ import division
import time
# Import the PCA9685 module.
import Adafruit_PCA9685
import RPi.GPIO as GPIO
# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
 
servo_pin = 15 #  servo connect to PWM 15

RIGHT = 465 #Steer servo car turn right
CENTER= 425 #Steer servo car go forward
LEFT = 385 #Steer servo car turn left

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)
pwm.set_pwm(servo_pin, 0, LEFT)
time.sleep(1)
pwm.set_pwm(servo_pin, 0, RIGHT)
time.sleep(1)
pwm.set_pwm(servo_pin, 0, CENTER)