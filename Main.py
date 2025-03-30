##############################################################
# Name: Chingiz, Thymmaythy and Jack
# Date: Spring 2025
# Description: Main file to run the programs with the RPi.GPIO library
##############################################################

# Import the necessary libraries
import RPi.GPIO as GPIO
import time
import pyaudio

# Main Code (Nothing specific to the program, just an example of GPIO usage for now)
"""
def main():
    # Set up GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)  # Example pin for output

    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    try:
        # Main loop
        while True:
            # Example: Blink an LED connected to pin 18
            GPIO.output(18, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(18, GPIO.LOW)
            time.sleep(1)

    except KeyboardInterrupt:
        print("Program terminated by user.")

    finally:
        # Clean up GPIO and PyAudio
        GPIO.cleanup()
        audio.terminate()"
"""