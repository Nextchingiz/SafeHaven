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

# Directory and file setup
USER_DATA_FILE = "user_data.json"
HISTORY_FOLDER = "Users_History"

if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, "w") as file:
        json.dump({}, file)

if not os.path.exists(HISTORY_FOLDER):
    os.makedirs(HISTORY_FOLDER)

current_user = None

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file)

def load_user_data():
    with open(USER_DATA_FILE, "r") as file:
        return json.load(file)

def get_user_history_file(username):
    return os.path.join(HISTORY_FOLDER, f"{username}_history.json")

def initialize_user_history(username):
    history_file = get_user_history_file(username)
    if not os.path.exists(history_file):
        with open(history_file, "w") as file:
            json.dump({"detections": []}, file)

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

def read_user_history(username):
    history_file = get_user_history_file(username)
    with open(history_file, "r") as file:
        return json.load(file)

def login():
    app = customtkinter.CTk()
    app.geometry("600x440")
    app.title('SafeHaven')

    img1 = ImageTk.PhotoImage(Image.open("assets/background.jpg"))
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
            app.destroy()
            show_home(username)
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    customtkinter.CTkButton(master=frame, width=220, text="Login", command=attempt_login, corner_radius=6).place(x=50, y=200)
    customtkinter.CTkButton(master=frame, width=220, text="Register", command=lambda: [app.destroy(), register()], corner_radius=6).place(x=50, y=290)

    app.mainloop()

def register():
    app = customtkinter.CTk()
    app.geometry("600x440")
    app.title('SafeHaven')

    img1 = ImageTk.PhotoImage(Image.open("assets/background.jpg"))
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
        app.destroy()
        login()

    customtkinter.CTkButton(master=frame, width=220, text="Register", command=submit_registration, corner_radius=6).place(x=50, y=330)

    app.mainloop()

def show_home(username):
    global home_mode
    user_data = load_user_data()
    detection_queue = Queue()

    app = customtkinter.CTk()
    app.geometry("600x440")
    app.title('SafeHaven')

    left_frame = customtkinter.CTkFrame(master=app, width=300)
    left_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, padx=10, pady=10)

    right_frame = customtkinter.CTkFrame(master=app, width=300)
    right_frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, padx=10, pady=10)

    customtkinter.CTkLabel(left_frame, text=f"Welcome, {username}", font=('Arial', 22)).pack(pady=10)
    customtkinter.CTkLabel(left_frame, text=f"Phone: {user_data[username]['phone']}", font=('Arial', 18)).pack(pady=5)
    customtkinter.CTkLabel(left_frame, text="Mode: Home Mode", font=('Arial', 18)).pack(pady=10)
    customtkinter.CTkLabel(left_frame, text="Press 5 seconds to activate Security Mode", font=('Arial', 16)).pack(pady=5)

    customtkinter.CTkLabel(right_frame, text="Detection History", font=('Arial', 22)).pack(pady=10)
    history_text = tkinter.Text(right_frame, wrap=tkinter.WORD, font=('Arial', 14))
    history_text.pack(fill=tkinter.BOTH, expand=True)

    def update_history():
        while not detection_queue.empty():
            detection = detection_queue.get()
            add_detection_to_history(username, detection)

        history_text.delete('1.0', tkinter.END)
        history = read_user_history(username)
        for detection in history["detections"]:
            history_text.insert(tkinter.END, f"{detection['timestamp']}: {detection['type']}\n")

        app.after(1000, update_history)

    def monitor_thread():
        monitor(detection_queue)

    Thread(target=monitor_thread, daemon=True).start()
    update_history()
    home_mode = True
    app.mainloop()

if __name__ == "__main__":
    login()
