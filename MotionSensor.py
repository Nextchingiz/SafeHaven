import RPi.GPIO as GPIO
import time

MOTION_SENSOR = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_SENSOR, GPIO.IN)

try:
    while True:
        if GPIO.input(MOTION_SENSOR):
            print("Motion detected!")
        else:
            print("No motion detected.")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()