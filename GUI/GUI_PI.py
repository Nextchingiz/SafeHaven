# This is the main GUI for the Rasp Pi

# Import libraries
import tkinter # For the GUI
import customtkinter # Make the GUI look better
from tkinter import messagebox # messageboxes
from PIL import ImageTk, Image # Images for the background and other things
import os # Create, check, delete folder, files, etc.
import json # Json files storing user data
import RPi.GPIO as GPIO
import time # Time
from datetime import datetime # Store the exact date and time something happens

# Set mode and theme for CustomTkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Directory and file setup: name the file with the user data, and the folder storing the user's history
USER_DATA_FILE = "user_data.json"
HISTORY_FOLDER = "Users_History"

# Check if we have already created a json file with the user's info, if not, create one
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as file:
        json.dump({}, file)

# Check if we have already a folder stroing json files with the user's history
if not os.path.exists(HISTORY_FOLDER):
    os.makedirs(HISTORY_FOLDER) # Make directory/folder

# Raspberry Pi GPIO setup
MOTION_SENSOR = 17
BUZZER = 18
BUTTON = 27
RED_LED = 22
GREEN_LED = 23

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTION_SENSOR, GPIO.IN)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)

# Set the home_mode to true, so it always starts like that
home_mode = True
current_user = None # No current user's, it will be set once the user logs into it's account

############
####JSON####
############

# Save user data
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

# Load user data
def load_user_data():
    with open(USER_DATA_FILE, "r") as file:
        return json.load(file)

# Get history file path for a user
def get_user_history_file(username):
    return os.path.join(HISTORY_FOLDER, f"{username}_history.json")

# Initialize a user's history file
def initialize_user_history(username):
    history_file = get_user_history_file(username)
    if not os.path.exists(history_file):
        with open(history_file, "w") as file:
            json.dump({"detections": []}, file)

# Add a detection to the user's history
def add_detection_to_history(username, detection_type):
    history_file = get_user_history_file(username)
    with open(history_file, "r") as file:
        history = json.load(file)

    detection_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": detection_type
    }
    history["detections"].append(detection_entry)

    with open(history_file, "w") as file:
        json.dump(history, file)

# Read user's detection history and update it whenever it is neededd
def read_user_history(username):
    history_file = get_user_history_file(username)
    with open(history_file, "r") as file:
        return json.load(file)

# Detection simulation (for demonstration purposes)
def simulate_detection(username):
    global home_mode
    while True:
        time.sleep(2)  # Simulate periodic checks
        if not home_mode:
            if GPIO.input(MOTION_SENSOR):  # Simulate motion detection
                add_detection_to_history(username, "Motion detected")
                GPIO.output(BUZZER, True)  # Trigger buzzer for a brief moment
                time.sleep(0.5)
                GPIO.output(BUZZER, False)

# Create the main app window
app = customtkinter.CTk()
app.geometry("600x440")
app.title('SafeHaven')

###############
#####PAGES#####
###############

# Login Page
def login():
    img1 = ImageTk.PhotoImage(Image.open("GUI/assets/background.jpg"))
    l1 = customtkinter.CTkLabel(master=app, image=img1)
    l1.pack()

    frame = customtkinter.CTkFrame(master=l1, width=320, height=360, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    customtkinter.CTkLabel(master=frame, text="Sign in SafeHaven", font=('Arial', 28)).place(x=50, y=45)
    customtkinter.CTkLabel(master=frame, text="Not signed in yet?", font=('Arial', 22)).place(x=70, y=250)

    entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
    entry1.place(x=50, y=110)

    entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
    entry2.place(x=50, y=155)

    def attempt_login():
        global current_user
        username = entry1.get()
        password = entry2.get()

        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            current_user = username
            initialize_user_history(username)
            messagebox.showinfo("Success", "Login successful!")
            show_home(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    customtkinter.CTkButton(master=frame, width=220, text="Login", command=attempt_login, corner_radius=6).place(x=50, y=200)
    customtkinter.CTkButton(master=frame, width=220, text="Register", command=register, corner_radius=6).place(x=50, y=290)

    app.mainloop()

# Register Page
def register():
    img1 = ImageTk.PhotoImage(Image.open("./assets/background.jpg"))
    l1 = customtkinter.CTkLabel(master=app, image=img1)
    l1.pack()

    frame = customtkinter.CTkFrame(master=l1, width=320, height=450, corner_radius=15)
    frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    customtkinter.CTkLabel(master=frame, text="Register in SafeHaven", font=('Arial', 28)).place(x=18, y=45)

    entry1 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Username')
    entry1.place(x=50, y=110)

    entry2 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Password', show="*")
    entry2.place(x=50, y=165)

    entry3 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Confirm Password', show="*")
    entry3.place(x=50, y=220)

    entry4 = customtkinter.CTkEntry(master=frame, width=220, placeholder_text='Phone Number')
    entry4.place(x=50, y=275)

    def submit_registration():
        username = entry1.get()
        password = entry2.get()
        confirm_password = entry3.get()
        phone = entry4.get()

        if not username or not password or not confirm_password or not phone:
            messagebox.showerror("Error", "All fields are required!")
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        user_data = load_user_data()
        if username in user_data:
            messagebox.showerror("Error", "Username already exists!")
            return

        user_data[username] = {"password": password, "phone": phone}
        save_user_data(user_data)
        initialize_user_history(username)
        messagebox.showinfo("Success", "Registration successful!")
        login()

    customtkinter.CTkButton(master=frame, width=220, text="Register", command=submit_registration, corner_radius=6).place(x=50, y=330)

# Home Page
def show_home(username):
    global home_mode
    user_data = load_user_data()

    app.destroy()
    home_window = customtkinter.CTk()
    home_window.geometry("600x440")
    home_window.title('SafeHaven')

    left_frame = customtkinter.CTkFrame(master=home_window, width=300)
    left_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=10, pady=10)

    right_frame = customtkinter.CTkFrame(master=home_window, width=300)
    right_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, padx=10, pady=10)

    customtkinter.CTkLabel(left_frame, text=f"Welcome, {username}", font=('Arial', 22)).pack(pady=10)
    customtkinter.CTkLabel(left_frame, text=f"Phone: {user_data[username]['phone']}", font=('Arial', 18)).pack(pady=5)
    customtkinter.CTkLabel(left_frame, text="Mode: Home Mode", font=('Arial', 18)).pack(pady=10)
    customtkinter.CTkLabel(left_frame, text="Press 5 seconds to activate Security Mode", font=('Arial', 16)).pack(pady=5)

    customtkinter.CTkLabel(right_frame, text="Detection History", font=('Arial', 22)).pack(pady=10)
    history_text = tkinter.Text(right_frame, wrap=tkinter.WORD, font=('Arial', 14))
    history_text.pack(fill=tkinter.BOTH, expand=True)

    def update_history():
        history_text.delete('1.0', tkinter.END)
        history = read_user_history(username)
        for detection in history["detections"]:
            history_text.insert(tkinter.END, f"{detection['timestamp']}: {detection['type']}\n")

    def monitor():
        update_history()
        if not home_mode:
            GPIO.output(GREEN_LED, False)
            GPIO.output(RED_LED, True)
        home_window.after(1000, monitor)

    home_mode = True
    GPIO.output(GREEN_LED, True)
    monitor()

    home_window.mainloop()

###############
######MAIN#####
###############

if __name__ == "__main__":
    login()