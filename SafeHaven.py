##############################################################
# Names: Chingiz, Thymmaythy, Jack
# Date: Spring 2025
# Description: SafeHaven
##############################################################

# Libraries for the GUI and the RPi.GPIO
import tkinter
import customtkinter
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import json
from datetime import datetime
import time
import RPi.GPIO as GPIO
from gpiozero import Buzzer

################
####HARDWARE####
################

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
security_message_displayed = False  # Makes sure security message shows once, ONLY ONCE

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_SENSOR, GPIO.IN)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(ULTRASONIC_1_TRIGGER, GPIO.OUT)
GPIO.setup(ULTRASONIC_1_ECHO, GPIO.IN)

# Turn on green LED (home mode) ALWAYS when starting the program
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
            
            # Blink red LED for 20 seconds (0.5-second intervals)
            for i in range(40):
                GPIO.output(RED_LED, True)
                time.sleep(0.25)  # Turn on for 0.25 seconds
                GPIO.output(RED_LED, False)
                time.sleep(0.25)  # Turn off for 0.25 seconds

            GPIO.output(RED_LED, True)  # Red LED stays on after blinking
            home_mode = False
            security_message_displayed = False  # Reset whenever a new mode is ACTIVATED
            print("Security mode is now ON!")  # Security Activation Message
            return  # Exit the loop

def alarm():
    """
    Turns on the alarm (buzzer). Or whatever we bought.
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
    Keeps the system running and helps to switch from one mode to another. Kind of a Main function
    """
    global message_displayed, security_message_displayed

    try:
        if not message_displayed:  # Show startup message once, ONCE DHKJDHJKSFHKJDFHSJK
            print("SafeHaven is active in home mode.")
            print("Hold the button for 5 seconds to activate security mode.")
            message_displayed = True

        while True:
            if home_mode:
                GPIO.output(GREEN_LED, True)  # Ensure green LED is on in home mode
                security_mode()  # Wait for whenever the security mode activation
            else:
                if not security_message_displayed:  # Show message once
                    print("Hold the button for 5 seconds to deactivate security mode.")
                    security_message_displayed = True

                deactivate_security_mode()  # Wait for mode deactivation again

                # Motion sensor
                if GPIO.input(MOTION_SENSOR):
                    print("Motion detected!")
                    add_detection_to_history(current_user, "Motion Detection")
                    alarm()

                # Ultrasonic sensor
                distance = get_distance(ULTRASONIC_1_TRIGGER, ULTRASONIC_1_ECHO)
                if distance < 10:  # Object within 10 cm
                    print("Ultrasonic sensor detected something!")
                    add_detection_to_history(current_user, "Ultrasonic Detection")
                    alarm()

            time.sleep(0.5)  # Adjust
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("System stopped. Cleaning up GPIO.")
        GPIO.output(RED_LED, False)
        GPIO.output(GREEN_LED, False)

##############
#####GUI######
##############

# Set mode and theme for CustomTkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Define global variables for the directory and file setup
USER_DATA_FILE = "user_data.json"
HISTORY_FOLDER = "Users_History"

# Check the existance of the user data json file, if not create it
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as file:
        json.dump({}, file)

# Check the existance of the user history file, if not create it
if not os.path.exists(HISTORY_FOLDER):
    os.makedirs(HISTORY_FOLDER) # Make directory

# Set the current user to None, it will be assigned a value once it logs in
current_user = None

# Save user data function
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

# load user data
def load_user_data():
    with open(USER_DATA_FILE, "r") as file:
        return json.load(file)

# Get the user's history file
def get_user_history_file(username):
    return os.path.join(HISTORY_FOLDER, f"{username}_history.json")

# Start/Initialize the user's specific Json history file
def initialize_user_history(username):
    history_file = get_user_history_file(username)
    if not os.path.exists(history_file):
        with open(history_file, "w") as file:
            json.dump({"detections": []}, file)

# Add detection to the history
def add_detection_to_history(username, detection_type):
    history_file = get_user_history_file(username)
    with open(history_file, "r") as file:
        history = json.load(file)
    detection_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": detection_type
    }
    history["detections"].append(detection_entry)

    # Save the updated history
    with open(history_file, "w") as file:
        json.dump(history, file, indent = 4)

# Read the user's history
def read_user_history(username):
    history_file = get_user_history_file(username) # Use the get function already defined above
    with open(history_file, "r") as file:
        return json.load(file)

# Login page/frame
def login():

    # General GUI info
    app = customtkinter.CTk()
    app.geometry("1280x720")
    app.title('SafeHaven')

    # Background image
    img1 = ImageTk.PhotoImage(Image.open("assets/background.jpg"))
    l1 = customtkinter.CTkLabel(master = app, image = img1)
    l1.pack()

    # Custom frame inside the GUI
    frame = customtkinter.CTkFrame(master = l1, width = 320, height = 360, corner_radius = 45, border_width = 5)
    frame.place(relx = 0.5, rely = 0.5, anchor = tkinter.CENTER)

    # Labels: Main text on the Top, and bottom registration text suggesting to click the registration button
    customtkinter.CTkLabel(master = frame, text = "Sign in SafeHaven", font = ('MS Sans Serif', 28)).place(x = 50, y = 45)
    customtkinter.CTkLabel(master = frame, text = "Not signed in yet?", font = ('MS Sans Serif', 22)).place(x = 70, y = 250)

    # Entry for the Username, including it's placeholder
    entry1 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Username', font = ('MS Sans Serif', 15))
    entry1.place(x = 50, y = 110)

    # Entry for the Username, including it's placeholder. It will show "*" whenever something is typed
    entry2 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Password', show = "*", font = ('MS Sans Serif', 15))
    entry2.place(x = 50, y = 155)

    # Attempt of login function (Not login exactly, because you have to try it first)
    def attempt_login():

        # Define the general variables
        global current_user # The "global" keyword should not be used, but I feel it is convinient in this case
        username = entry1.get()
        password = entry2.get()

        # Define the program functionality

        # Load the user file
        user_data = load_user_data()

        # Check if the username and password provided are the same as the ones stored in the user data Json file
        if username in user_data and user_data[username]["password"] == password:
            current_user = username
            initialize_user_history(username) # If it is true, start the user history file, to start storing data
            messagebox.showinfo("Success", "Login successful!") # Small messagebox informing about the successful attempt
            app.destroy() # Destroy/close the login page
            main(username) # Start the main program (the function is defined below)
        else:
            messagebox.showerror("Error", "Invalid username or password!") # Error if the username and/or password are not the same

    # Button for the Login
    customtkinter.CTkButton(master = frame, width = 220, text = "Login", command = attempt_login, corner_radius = 6, font = ('MS Sans Serif', 15)).place(x = 50, y = 200)

    # Button for the Registration
    customtkinter.CTkButton(master = frame, width = 220, text = "Register", command = lambda: [app.destroy(), register()], corner_radius = 6, font = ('MS Sans Serif', 15)).place(x = 50, y = 290)

    # Mainloop to run the Login page
    app.mainloop()

# Define the registration frame/page
def register():

    # Define the general variables
    app = customtkinter.CTk()
    app.geometry("1280x720")
    app.title('SafeHaven')

    # Background image, same as before in the Login page
    img1 = ImageTk.PhotoImage(Image.open("assets/background.jpg"))
    l1 = customtkinter.CTkLabel(master = app, image = img1)
    l1.pack()

    # Small Frame inside the GUI itself, as before
    frame = customtkinter.CTkFrame(master = l1, width = 320, height = 450, corner_radius = 45)
    frame.place(relx = 0.5, rely = 0.5, anchor = tkinter.CENTER) # Center the frame in the page

    # Label for the general message on top, just as a welcoming message
    customtkinter.CTkLabel(master = frame, text = "Register in SafeHaven", font = ('MS Sans Serif', 28)).place(x = 18, y = 45)

    # Entry for the Username, with a placeholder
    entry1 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Username', font = ('MS Sans Serif', 15))
    entry1.place(x = 50, y = 110)

    # Entry for the Password, including it's placeholder
    entry2 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Password', show = "*", font = ('MS Sans Serif', 15))
    entry2.place(x = 50, y = 165)

    # Entry for the Confirm Password, including it's placeholder
    entry3 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Confirm Password', show = "*", font = ('MS Sans Serif', 15))
    entry3.place(x = 50, y = 220)

    # Entry for the Phone Number, including it's placeholder
    entry4 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Phone Number', font = ('MS Sans Serif', 15))
    entry4.place(x = 50, y = 275)

    # Define a submit registration function, why not just registration? Well, same as before, it's an attempt.
    def submit_registration():

        # Define the general variables by just referring to the values we received in the "form"
        username = entry1.get()
        password = entry2.get()
        confirm_password = entry3.get()
        phone = entry4.get()

        # Check if there is some information missing
        if not username or not password or not confirm_password or not phone:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Check if both of the passwords entered are the same
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Check if there is already an existing username with that same name that was typed in the form
        user_data = load_user_data()
        if username in user_data:
            messagebox.showerror("Error", "Username already exists!")
            return

        # Add these values to the Json file with the user data
        """
        user_data[username] = {"password": password, "phone": phone}
        save_user_data(user_data)
        initialize_user_history(username)
        """

        user_data[username] = {"password": password, "phone": phone}
        with open("user_data.json", "w") as file:
            json.dump(user_data, file, indent=4)

        # Create history file for user
        history_path = os.path.join(HISTORY_FOLDER, f"{username}_history.json")
        with open(history_path, "w") as file:
            json.dump({"detections": []}, file)

        messagebox.showinfo("Success", "Registration successful!")
        app.destroy()
        login()

    # Button to Register
    customtkinter.CTkButton(master = frame, width = 220, text = "Register", command = submit_registration, corner_radius = 6, font = ('MS Sans Serif', 15)).place(x = 50, y = 330)

    # Maimloop
    app.mainloop()

#############
####MAIN#####
#############

# Define the function to show the home page/frame
def main(username):

    # Define the global variables
    user_data = load_user_data()

    # Define a function to update the detection history
    # def update_history():
        # add_detection_to_history(username, detection)

    # Start the monitor function, that starts the hardware RPi GPIO
    monitor()

# Start the program
if __name__ == "__main__":
    login()
