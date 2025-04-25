# This in the GUI for the class DEMO
# It emulates detections

# Import libraries
import os
import json # For th
import tkinter
import customtkinter
from datetime import datetime
from PIL import ImageTk, Image

# Set Mode and Theme in CustomTkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# Globals
current_user = None  # To track the logged-in user
HISTORY_FOLDER = "Users_History"

# Ensure the Users_History folder exists
if not os.path.exists(HISTORY_FOLDER):
    os.makedirs(HISTORY_FOLDER)

# Function to log detections
def log_detection(username, detection_type):
    file_path = os.path.join(HISTORY_FOLDER, f"{username}_history.json")
    # Read existing history or create new
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            history = json.load(file)
    else:
        history = {"detections": []}
    # Add detection
    detection_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": detection_type
    }
    history["detections"].append(detection_entry)
    # Save updated history
    with open(file_path, "w") as file:
        json.dump(history, file, indent=4)

# Simulate a detection
def simulate_detection():
    if current_user:
        log_detection(current_user, "Simulated Detection")
        update_history()

# Function to update history section
def update_history():
    if current_user:
        file_path = os.path.join(HISTORY_FOLDER, f"{current_user}_history.json")
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                history = json.load(file)
            # Safely extract timestamp and type
            history_text = "\n".join([
                f"{entry.get('timestamp', 'Unknown Time')}: {entry.get('type', 'Unknown Type')}"
                for entry in history.get("detections", [])
            ])
        else:
            history_text = "No detections yet."
        history_label.configure(text=history_text)

# GUI Functions

# Log in User
def login_user():
    global current_user
    username = login_username.get()
    password = login_password.get()

    # Validate user
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as file:
            users = json.load(file)
        if username in users and users[username]["password"] == password:
            current_user = username
            show_home()
            return
    error_label.configure(text="Invalid username or password!")

# Register user
def register_user():
    username = register_username.get()
    password = register_password.get()
    confirm_password = register_confirm_password.get()
    phone = register_phone.get()

    # Validate inputs
    if not username or not password or not confirm_password or not phone:
        register_error_label.configure(text="All fields are required!")
        return
    if password != confirm_password:
        register_error_label.configure(text="Passwords do not match!")
        return

    # Save to user_data.json
    if os.path.exists("user_data.json"):
        with open("user_data.json", "r") as file:
            users = json.load(file)
    else:
        users = {}

    if username in users:
        register_error_label.configure(text="Username already exists!")
        return

    users[username] = {"password": password, "phone": phone}
    with open("user_data.json", "w") as file:
        json.dump(users, file, indent=4)

    # Create history file for user
    history_path = os.path.join(HISTORY_FOLDER, f"{username}_history.json")
    with open(history_path, "w") as file:
        json.dump({"detections": []}, file)

    show_login()

# Show login
def show_login():
    register_frame.pack_forget()
    home_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)

# Show register
def show_register():
    login_frame.pack_forget()
    home_frame.pack_forget()
    register_frame.pack(fill="both", expand=True)

# Show home
def show_home():
    login_frame.pack_forget()
    register_frame.pack_forget()
    user_info_label.configure(text=f"User: {current_user}")
    mode_info_label.configure(text="Mode: Home")
    home_frame.pack(fill="both", expand=True)
    update_history()

# Main App
app = customtkinter.CTk()
app.geometry("800x600")
app.title("SafeHaven")

# Background Image
bg_image = Image.open("assets/background.jpg")
bg_image = ImageTk.PhotoImage(bg_image)

bg_label = tkinter.Label(app, image=bg_image)
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

# Small Frame
small_frame = customtkinter.CTkFrame(app, width=500, height=400, corner_radius=15)
small_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Login Frame (Inside Small Frame)
login_frame = customtkinter.CTkFrame(small_frame, width=500, height=400)
login_frame.pack(fill="both", expand=True)

login_username = customtkinter.CTkEntry(login_frame, placeholder_text="Username")
login_username.pack(pady=10)

login_password = customtkinter.CTkEntry(login_frame, placeholder_text="Password", show="*")
login_password.pack(pady=10)

login_button = customtkinter.CTkButton(login_frame, text="Login", command=login_user)
login_button.pack(pady=10)

register_button = customtkinter.CTkButton(login_frame, text="Register", command=show_register)
register_button.pack(pady=10)

error_label = customtkinter.CTkLabel(login_frame, text="", text_color="red")
error_label.pack(pady=5)

# Register Frame (Inside Small Frame)
register_frame = customtkinter.CTkFrame(small_frame)

register_username = customtkinter.CTkEntry(register_frame, placeholder_text="Username")
register_username.pack(pady=10)

register_password = customtkinter.CTkEntry(register_frame, placeholder_text="Password", show="*")
register_password.pack(pady=10)

register_confirm_password = customtkinter.CTkEntry(register_frame, placeholder_text="Confirm Password", show="*")
register_confirm_password.pack(pady=10)

register_phone = customtkinter.CTkEntry(register_frame, placeholder_text="Phone Number")
register_phone.pack(pady=10)

register_register_button = customtkinter.CTkButton(register_frame, text="Register", command=register_user)
register_register_button.pack(pady=10)

register_error_label = customtkinter.CTkLabel(register_frame, text="", text_color="red")
register_error_label.pack(pady=5)

# Home Frame
home_frame = customtkinter.CTkFrame(small_frame)

user_info_label = customtkinter.CTkLabel(home_frame, text="User:")
user_info_label.pack(pady=10)

mode_info_label = customtkinter.CTkLabel(home_frame, text="Mode:")
mode_info_label.pack(pady=10)

simulate_button = customtkinter.CTkButton(home_frame, text="Simulate Detection", command=simulate_detection)
simulate_button.pack(pady=10)

history_label = customtkinter.CTkLabel(home_frame, text="History:")
history_label.pack(pady=10)

# Show Login Initially
show_login()

# Mainloop
app.mainloop()