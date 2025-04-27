# GUI for the Raspberry PI

# Libraries for the GUI
import tkinter
import customtkinter
from tkinter import messagebox
from PIL import ImageTk, Image
import os
import json
from datetime import datetime
from threading import Thread
import time
from queue import Queue
from main import monitor

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
    frame = customtkinter.CTkFrame(master = l1, width = 320, height = 360, corner_radius = 45)
    frame.place(relx = 0.5, rely = 0.5, anchor = tkinter.CENTER)

    # Labels: Main text on the Top, and bottom registration text suggesting to click the registration button
    customtkinter.CTkLabel(master = frame, text = "Sign in SafeHaven", font = ('Arial', 28)).place(x = 50, y = 45)
    customtkinter.CTkLabel(master = frame, text = "Not signed in yet?", font = ('Arial', 22)).place(x = 70, y = 250)

    # Entry for the Username, including it's placeholder
    entry1 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Username')
    entry1.place(x = 50, y = 110)

    # Entry for the Username, including it's placeholder. It will show "*" whenever something is typed
    entry2 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Password', show = "*")
    entry2.place(x=50, y=155)

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
            show_home(username) # Start the home page for that specific user (the function is defined below)
        else:
            messagebox.showerror("Error", "Invalid username or password!") # Error if the username and/or password are not the same

    # Button for the Login
    customtkinter.CTkButton(master = frame, width = 220, text = "Login", command = attempt_login, corner_radius = 6).place(x = 50, y = 200)

    # Button for the Registration
    customtkinter.CTkButton(master = frame, width = 220, text = "Register", command = lambda: [app.destroy(), register()], corner_radius = 6).place(x = 50, y = 290)

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
    customtkinter.CTkLabel(master = frame, text = "Register in SafeHaven", font = ('Arial', 28)).place(x = 18, y = 45)

    # Entry for the Username, with a placeholder
    entry1 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Username')
    entry1.place(x = 50, y = 110)

    # Entry for the Password, including it's placeholder
    entry2 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Password', show = "*")
    entry2.place(x = 50, y = 165)

    # Entry for the Confirm Password, including it's placeholder
    entry3 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Confirm Password', show = "*")
    entry3.place(x = 50, y = 220)

    # Entry for the Phone Number, including it's placeholder
    entry4 = customtkinter.CTkEntry(master = frame, width = 220, placeholder_text = 'Phone Number')
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
        messagebox.showinfo("Success", "Registration successful!")
        app.destroy()
        login()
        """

        user_data[username] = {"password": password, "phone": phone}
        with open("user_data.json", "w") as file:
            json.dump(user_data, file, indent=4)

        # Create history file for user
        history_path = os.path.join(HISTORY_FOLDER, f"{username}_history.json")
        with open(history_path, "w") as file:
            json.dump({"detections": []}, file)

    # Button to Register
    customtkinter.CTkButton(master = frame, width = 220, text = "Register", command = submit_registration, corner_radius = 6).place(x = 50, y = 330)

    # Maimloop
    app.mainloop()

# Define the function to show the home page/frame
def show_home(username):

    # Define the global variables
    global home_mode
    user_data = load_user_data()
    detection_queue = Queue()

    # General page/frame values
    app = customtkinter.CTk()
    app.geometry("1280x720")
    app.title('SafeHaven')

    # Generate the background image

    img1 = ImageTk.PhotoImage(Image.open("assets/background.jpg"))
    l1 = customtkinter.CTkLabel(master = app, image = img1)
    l1.pack()

    # Generate the Top frame for the User info
    top_frame = customtkinter.CTkFrame(master = l1, width = 1280/2)
    top_frame.place(side = tkinter.TOP, fill = tkinter.BOTH, padx = 10, pady = 10)

    # Labels for the top frame
    customtkinter.CTkLabel(top_frame, text = f"Welcome, {username}", font = ('Arial', 22)).pack(pady = 10)
    customtkinter.CTkLabel(top_frame, text = f"Phone: {user_data[username]['phone']}", font = ('Arial', 18)).pack(pady = 5)
    customtkinter.CTkLabel(top_frame, text = "Mode: Home Mode", font = ('Arial', 18)).pack(pady = 10)
    customtkinter.CTkLabel(top_frame, text = "Press 5 seconds to activate Security Mode", font = ('Arial', 16)).pack(pady = 5)

    # Generate the Bottom frame for the history
    bottom_frame = customtkinter.CTkFrame(master = l1, width = 1280/2)
    bottom_frame.place(side = tkinter.BOTTOM, fill = tkinter.BOTH, padx = 10, pady = 10)

    # Labels for the bottom frame
    customtkinter.CTkLabel(bottom_frame, text = "Detection History", font = ('Arial', 22)).pack(pady = 10)
    history_text = tkinter.Text(bottom_frame, wrap = tkinter.WORD, font = ('Arial', 14))
    history_text.pack(fill = tkinter.BOTH, expand = True)

    # Define a function to update the detection history
    def update_history():
        while not detection_queue.empty():
            detection = detection_queue.get()
            add_detection_to_history(username, detection)

        history_text.delete('1.0', tkinter.END)
        history = read_user_history(username)
        for detection in history["detections"]:
            history_text.insert(tkinter.END, f"{detection['timestamp']}: {detection['type']}\n")

        app.after(1000, update_history)
    
    # Start the monitor function, that starts the hardware RPi GPIO
    def monitor_thread():
        monitor(detection_queue)

    Thread(target=monitor_thread, daemon=True).start()
    update_history()
    home_mode = True
    app.mainloop()

# Start the program
if __name__ == "__main__":
    login()
