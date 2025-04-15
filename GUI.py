"""This is the GUI Program that will start whenever we start the program"""

# Import the necessary libraries
import tkinter as tk # Simply import tkinter
from tkinter import messagebox # Small message boxes that appear
import os
import json # Json for storing user information and further using it for the Flask web app

# Import the necessary files
from Main.py import home_mode

# Path to the user data file where we will store the info
USER_DATA_FILE = "user_data.json"

# Check if the user data file exists, if not, create one
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as file:
        json.dump({}, file)

# Save user data to the file
def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

# Load user data from the file
def load_user_data():
    with open(USER_DATA_FILE, "r") as file:
        return json.load(file)

# Registration screen in case our user has not set a user and password yet
def register():
    def submit_registration():
        username = username_entry.get() # Type in the desired username
        password = password_entry.get() # Type in the password
        confirm_password = confirm_password_entry.get() # Ask for the password again to confirm it
        phone = phone_entry.get() # Type in the phone number to which the notifications are going to be sent

        # Define the situation in which any of the things we ask for is presented to the program. If something is missing, ERROR.
        if not username or not password or not confirm_password or not phone:
            messagebox.showerror("Error", "All fields are required")
            return

        # Define the situation in which the password confirmation is not the same as the password
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return

        # Define the situation in which the desired username is already stored in our system for someone else
        user_data = load_user_data()
        if username in user_data:
            messagebox.showerror("Error", "Username already exists")
            return

        user_data[username] = {"password": password, "phone": phone} # Add the info to the JSON file we created
        save_user_data(user_data) # Save the info
        messagebox.showinfo("Success", "Registration successful!") # Once we saved the info, we show a confirmation message box
        register_window.destroy() # Destroy the window

    register_window = tk.Toplevel() 
    register_window.title("Register") 

    """
    Now, we create all the labels an buttons for the program.
    """

    # Label for username
    tk.Label(register_window, text = "Username:").grid(row=0, column=0, padx=10, pady=5) # Design of the label
    username_entry = tk.Entry(register_window) # Enter the info
    username_entry.grid(row = 0, column = 1, padx = 10, pady = 5)

    # Label for Password
    tk.Label(register_window, text = "Password:").grid(row = 1, column = 0, padx = 10, pady = 5) # Design of the label
    password_entry = tk.Entry(register_window, show = "*") # Enter the info
    password_entry.grid(row = 1, column = 1, padx = 10, pady = 5)

    # Label for Confirm Password
    tk.Label(register_window, text = "Confirm Password:").grid(row = 2, column = 0, padx = 10, pady = 5) # Design of the Label
    confirm_password_entry = tk.Entry(register_window, show = "*") # Enter the info
    confirm_password_entry.grid(row = 2, column = 1, padx = 10, pady = 5)

    # Label for the Phone number
    tk.Label(register_window, text = "Phone Number:").grid(row = 3, column = 0, padx = 10, pady = 5) # Design of the Label
    phone_entry = tk.Entry(register_window) # Enter the info
    phone_entry.grid(row = 3, column = 1, padx = 10, pady = 5)

    # Button for submitting the info
    tk.Button(register_window, text = "Submit", command = submit_registration).grid(row = 4, columnspan = 2, pady = 10)

# SafeHaven status screen that will inform the user of the status
def safehaven_status(username):
    def update_status():
        # Example of updating the status of the screen (When going from home mode to security mode, or viceversa)
        mode_label.config(text = f"Mode: {'Home Mode' if home_mode else 'Security Mode'}")
        threat_label.config(text = f"Threat: {'None' if not threat_detected else 'Intruder detected!'}")

    # Define the window
    safehaven_window = tk.Toplevel()
    safehaven_window.title("SafeHaven") # Define the title

    # Create the labels for the SafeHaven text on top of the page, and the "Welcome" sign.
    tk.Label(safehaven_window, text = "SafeHaven", font = ("Arial", 20)).pack(pady = 10)
    tk.Label(safehaven_window, text = f"Welcome, {username}").pack(pady = 5)

    # Create the labels for the different modes we have:

    # Home Mode
    mode_label = tk.Label(safehaven_window, text = "Mode: Home Mode", font = ("Arial", 14))
    mode_label.pack(pady = 5)

    # Security Mode
    threat_label = tk.Label(safehaven_window, text = "Threat: None", font = ("Arial", 14))
    threat_label.pack(pady = 5)

    # Button to refresh whenever we press the button for 5 seconds and change in between modes
    tk.Button(safehaven_window, text = "Refresh Status", command = update_status).pack(pady = 10)

# Login screen for those who are already successfully registered in the system.
def login():

    def attempt_login():
        username = username_entry.get() # Get the username
        password = password_entry.get() # Get the password

        # Check the data and compare the info we receive in the login screen with what we got stored in the json file
        user_data = load_user_data()
        if username in user_data and user_data[username]["password"] == password:
            messagebox.showinfo("Success", "Login successful!") # If they match, success
            login_window.destroy()
            safehaven_status(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!") # If they do not, Ups

    # Define the window and the title "Login"
    login_window = tk.Toplevel()
    login_window.title("Login")

    # Create the labels for the info we are asking for:

    # Label for the username
    tk.Label(login_window, text = "Username:").grid(row = 0, column = 0, padx = 10, pady = 5)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row = 0, column = 1, padx = 10, pady = 5)

    # Label for the password
    tk.Label(login_window, text = "Password:").grid(row = 1, column = 0, padx = 10, pady = 5)
    password_entry = tk.Entry(login_window, show = "*")
    password_entry.grid(row = 1, column = 1, padx = 10, pady = 5)

    # Button for submitting the info
    tk.Button(login_window, text = "Login", command = attempt_login).grid(row = 2, columnspan = 2, pady = 10)

# Main GUI program
root = tk.Tk()
root.title("SafeHaven System")

# Defaul text that will appear whenever we open the program

# Label for the "Welcome to SafeHaven" welcoming message
tk.Label(root, text = "Welcome to SafeHaven", font = ("Arial", 20)).pack(pady = 10)

# Button to be redirected to the login screen
tk.Button(root, text = "Login", command = login).pack(pady = 5)

# Button to be redirected to the first time registration screen
tk.Button(root, text = "Register", command = register).pack(pady = 5)

# Mainloop
root.mainloop()