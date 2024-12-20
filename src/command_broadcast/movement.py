#  ___   ___  ___  _   _  ___   ___   ____ ___  ____  
# / _ \ /___)/ _ \| | | |/ _ \ / _ \ / ___) _ \|    \ 
#| |_| |___ | |_| | |_| | |_| | |_| ( (__| |_| | | | |
# \___/(___/ \___/ \__  |\___/ \___(_)____)___/|_|_|_|
#                  (____/ 
# Osoyoo Model-Pi L298N DC motor driver programming guide
# tutorial url: https://osoyoo.com/2020/03/01/python-programming-tutorial-model-pi-l298n-motor-driver-for-raspberry-pi/

from __future__ import division
import time
#Import the PCA9685 module.
import Adafruit_PCA9685
import RPi.GPIO as GPIO
# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
 
servo_pin = 15 #  servo connect to PWM 15

RIGHT = 500 #Steer servo car turn right
CENTER= 425 #Steer servo car go forward
LEFT = 385 #Steer servo car turn left

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

move_speed = 4000  # Max pulse length out of 4096

# Set frequency to 60hz, good for servos.
#pwm.set_pwm_freq(60)
#pwm.set_pwm(servo_pin, 0, LEFT)
#time.sleep(1)
#pwm.set_pwm(servo_pin, 0, RIGHT)
#time.sleep(1)
#pwm.set_pwm(servo_pin, 0, CENTER)


GPIO.setmode(GPIO.BCM) # GPIO number  in BCM mode
GPIO.setwarnings(False)
#define L298N(Model-Pi motor drive board) GPIO pins
IN1 = 23  #right motor direction pin
IN2 = 24  #right motor direction pin
IN3 = 27  #left motor direction pin
IN4 = 22  #left motor direction pin
ENA = 0  #Right motor speed PCA9685 port 0
ENB = 1  #Left motor speed PCA9685 port 1

# Define motor control  pins as output
GPIO.setup(IN1, GPIO.OUT)   
GPIO.setup(IN2, GPIO.OUT) 
GPIO.setup(IN3, GPIO.OUT)   
GPIO.setup(IN4, GPIO.OUT) 

def changespeed(speed):
	pwm.set_pwm(ENA, 0, speed)
	pwm.set_pwm(ENB, 0, speed)

def stopcar():
	GPIO.output(IN1, GPIO.LOW)
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(IN3, GPIO.LOW)
	GPIO.output(IN4, GPIO.LOW)
	changespeed(0)


def forward():
	GPIO.output(IN1, GPIO.HIGH)
	GPIO.output(IN2, GPIO.LOW)
	GPIO.output(IN3, GPIO.HIGH)
	GPIO.output(IN4, GPIO.LOW)
	changespeed(move_speed)
 
	#following two lines can be removed if you want car make continuous movement without pause
	#time.sleep(0.25)  
	#stopcar()
	
def backward():
	GPIO.output(IN1, GPIO.LOW)
	GPIO.output(IN2, GPIO.HIGH)
	GPIO.output(IN3, GPIO.LOW)
	GPIO.output(IN4, GPIO.HIGH)

	changespeed(move_speed)
	#following two lines can be removed if you want car make continuous movement without pause
	#time.sleep(0.25)  
	#stopcar()
	
def steer(angle):
	if angle>RIGHT :
		angle=RIGHT
	if angle<LEFT :
		angle=LEFT
	pwm.set_pwm(servo_pin, 0, angle)
	print("Angle: ", angle)
if __name__ == "__main__":
	steer(CENTER)	
	forward()
	time.sleep(2)  
	stopcar()
	time.sleep(0.25)

	backward()
	time.sleep(2)  
	stopcar()
	time.sleep(0.25) 

	steer(LEFT)
	forward()
	time.sleep(2)  
	
	steer(RIGHT)
	forward()
	time.sleep(2)  

	backward()
	time.sleep(2)  

	steer(LEFT)
	backward()
	time.sleep(2)  
	stopcar()
	steer(CENTER)	

	time.sleep(2)
	pwm.set_pwm(15, 0, 0)
