##############################################################
# Names: Chingiz, Thymmaythy, Jack
# Date: Spring 2025
# Description: SafeHaven
##############################################################

import RPi.GPIO as GPIO # Import the GPIO library for Raspberry Pi
import time # Import time library for measuring time
#from playsound import playsound # Import playsound library for playing alarm sound

# GPIO Pin Setup (These are just example GPIO numbers, we will adjust them as needed)
MOTION_SENSOR = 17
BUZZER = 18
BUTTON = 27
RED_LED = 23
GREEN_LED = 22
ULTRASONIC_1_TRIGGER = 5
ULTRASONIC_1_ECHO = 6
ULTRASONIC_2_TRIGGER = 13
ULTRASONIC_2_ECHO = 19

home_mode = True  # Start in home mode by default

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_SENSOR, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(ULTRASONIC_1_TRIGGER, GPIO.OUT)
GPIO.setup(ULTRASONIC_1_ECHO, GPIO.IN)
GPIO.setup(ULTRASONIC_2_TRIGGER, GPIO.OUT)
GPIO.setup(ULTRASONIC_2_ECHO, GPIO.IN)

def security_mode():
    global home_mode
    print("Press and hold the button for 5 seconds to activate security mode")
    start_time = time.time()
    while GPIO.input(BUTTON) == 0:
        if time.time() - start_time >= 5: # Button pressed for 5 seconds, if not, no action
            print("Security mode activation in 20 seconds")
            time.sleep(20) # Wait for 20 seconds to allow user to leave the place
            home_mode = False # Set home mode to False
            GPIO.output(RED_LED, False) # Turn off red LED
            GPIO.output(GREEN_LED, True) # Turn on green LED
            print("Security mode activated!")
            return

def alarm():
    GPIO.output(BUZZER, GPIO.HIGH)
    #playsound("alarm.mp3") # Play alarm sound (We will need to add the sound file later, with the name "alarm.mp3")
    time.sleep(2) # Alarm duration for now, we can adjust it later
    GPIO.output(BUZZER, GPIO.LOW)

def get_distance(trigger, echo):
    GPIO.output(trigger, True)
    time.sleep(0.00001) # Trigger the ultrasonic sensor
    GPIO.output(trigger, False)
    
    start_time = time.time()
    stop_time = time.time()
    
    while GPIO.input(echo) == 0:
        start_time = time.time()
    while GPIO.input(echo) == 1:
        stop_time = time.time()
    
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Convert to cm (because 34300 cm/s is the speed of sound)
    return distance

def monitor(): # Monitor for motion and ultrasonic sensor input
    try:
        while True:
            security_mode() # Check if the button is pressed to activate security mode
            if home_mode:
                continue
            
            if GPIO.input(MOTION_SENSOR): # Check for motion detection
                print("Motion detected!")
                alarm()
            
            distance1 = get_distance(ULTRASONIC_1_TRIGGER, ULTRASONIC_1_ECHO) # Get distance from first ultrasonic sensor
            distance2 = get_distance(ULTRASONIC_2_TRIGGER, ULTRASONIC_2_ECHO) # Get distance from second ultrasonic sensor
            
            if distance1 < 50 or distance2 < 50:
                print("Object detected by ultrasonic sensor!") # If an object is detected within 50 cm, trigger the alarm
                alarm()
            
            time.sleep(0.5) # Adjust the sleep time as needed for the application later
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("System Stopped")


# Run the system
if __name__ == "__main__":
    print("Safe Haven system activated in home mode.")
    monitor()
    GPIO.cleanup()
