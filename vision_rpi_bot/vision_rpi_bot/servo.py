import RPi.GPIO as GPIO
import time

servoPIN = 14
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(0) # Initialization
duty = 2
#p.ChangeDutyCycle(1)
#time.sleep(1)
p.ChangeDutyCycle(2)
time.sleep(0.5)
p.ChangeDutyCycle(12)
time.sleep(0.3)
p.ChangeDutyCycle(2)
time.sleep(0.1)
p.ChangeDutyCycle(0)
p.stop()
GPIO.cleanup()