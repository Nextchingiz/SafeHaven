##############################################################
# Names: Chingiz, Thymmaythy, Jack
# Date: Spring 2025
# Description: SafeHaven
##############################################################

import RPi.GPIO as GPIO
from gpiozero import Buzzer
import time

# GPIO Pins
MOTION_SENSOR = 17
buzzer = Buzzer(18) # Buzzer through gpiozero library
BUTTON = 27
RED_LED = 22
GREEN_LED = 23
ULTRASONIC_1_TRIGGER = 5
ULTRASONIC_1_ECHO = 6

home_mode = True  # System starts in home mode ALWAYS
message_displayed = False  # Makes sure startup message shows once, ONLY ONCE
security_message_displayed = False  # akes sure security message shows once, ONLY ONCE

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_SENSOR, GPIO.IN)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(ULTRASONIC_1_TRIGGER, GPIO.OUT)
GPIO.setup(ULTRASONIC_1_ECHO, GPIO.IN)

# Turn on green LED (home mode) ALWAYS when sttarting the program
GPIO.output(RED_LED, False)
GPIO.output(GREEN_LED, True)

def security_mode():
    """
    Turns on security mode if the button is pressed for 5 seconds.
    """
    global home_mode, security_message_displayed
    start_time = time.time()

    while GPIO.input(BUTTON) == 0:  # While button is pressed
        if time.time() - start_time >= 5:  # Check for 5 seconds
            print("Starting security mode in 20 seconds...")
            GPIO.output(GREEN_LED, False)  # Turn off green LED
            for i in range(40):  # Blink red LED for 20 seconds, until security mode starts, 40 times because 20/0.5 = 40 times
                GPIO.output(RED_LED, True)
                time.sleep(0.5)
                GPIO.output(RED_LED, False)

            GPIO.output(RED_LED, True)  # Red LED stays on, ON
            home_mode = False
            security_message_displayed = False  # Reset whenever the new mode is ACTIVATED
            print("Security mode is now ON!") # Security Activation Message
            return # Loop

def alarm():
    """
    Turns on the alarm (buzzer). Or wahtever we bought.
    """
    buzzer.on()
    time.sleep(0.5)
    buzzer.off()
    time.sleep(0.5)

def get_distance(trigger, echo):
    """
    Measures distance using the ultrasonic sensor and basic physics laws.
    """
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo) == 0:
        start_time = time.time()
    while GPIO.input(echo) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    return (elapsed_time * 34300) / 2  # Distance in cm, because 34300 is the speed of sound

def deactivate_security_mode():
    """
    Turns off security mode if button is held for 5 seconds.
    """
    global home_mode # It should not be done, but I define it with the keyword global to use in other places of the program.
    #print("Hold the button for 5 seconds to stop security mode.")
    start_time = time.time()

    while GPIO.input(BUTTON) == 0:  # While button is pressed
        if time.time() - start_time >= 5:  # Hold button (check) for 5 seconds
            home_mode = True
            GPIO.output(RED_LED, False)
            GPIO.output(GREEN_LED, True)
            print("SECURITY MODE OFF. HOME MODE ACTIVATED")
            return

def monitor():
    """
    Keeps the system running and helps to swtich from one mode to another. Kind of a Main function
    """
    global message_displayed, security_message_displayed

    try:
        if not message_displayed:  # Show startup message once, ONCE DHKJDHJKSFHKJDFHSJK
            print("SafeHaven is active in home mode.")
            print("Hold the button for 5 seconds to activate security mode.")
            message_displayed = True

        while True:
            if home_mode:
                security_mode()  # Wait for whenever the security mode activation
            else:
                if not security_message_displayed:  # Show message once
                    print("Hold the button for 5 seconds to deactivate security mode.")
                    security_message_displayed = True

                deactivate_security_mode()  # Wait for mode deactivation again

                # Motion sensor
                if GPIO.input(MOTION_SENSOR):
                    print("Motion detected!")
                    alarm()

                # Ultrasonic sensor
                distance = get_distance(ULTRASONIC_1_TRIGGER, ULTRASONIC_1_ECHO)
                if distance < 10:  # Object within 10 cm
                    print("Ultrasonic sensor detected something!")
                    alarm()

            time.sleep(0.5)  # Adjust
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("System stopped. Cleaning up GPIO.")
        GPIO.output(RED_LED, False)
        GPIO.output(GREEN_LED, False)

# Run the system
if __name__ == "__main__":
    #print("Hold the button for 5 seconds to start security mode.")
    monitor()
